from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff
from django.db import IntegrityError, connection
from datetime import date
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Staff, Appointment 

def _get_staff_appointments_by_search(staff_id, query):
    sql = """
        SELECT
            a.appointment_id,                  -- PK for .raw()
            a.appointment_id AS id,
            a.appointment_date AS date,
            a.start_time       AS start,
            a.end_time         AS end,
            a.status,
            a.total_amount     AS total,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            r.review_id        AS review_id,
            r.rating           AS review_rating,
            r.comment          AS review_comment      -- NEW
        FROM appointment a
        JOIN customer c
          ON c.customer_id = a.customer_id
        LEFT JOIN review r
          ON r.appointment_id = a.appointment_id
         AND r.staff_id       = a.staff_id
        WHERE a.staff_id = %s
    """
    params = [staff_id]

    if query:
        sql += """
          AND (
                a.status LIKE %s OR
                c.first_name LIKE %s OR
                c.last_name  LIKE %s OR
                CONCAT(c.first_name,' ',c.last_name) LIKE %s
          )
        """
        like = f"%{query}%"
        params += [like, like, like, like]

    sql += " ORDER BY a.appointment_date DESC, a.start_time DESC, a.appointment_id DESC "
    return Appointment.objects.raw(sql, params)


@login_required
def staff_my_appointments(request):
    # Require an authenticated staff user linked to STAFF.user_id
    if not request.user.is_staff:
        return redirect('home')

    staff = get_object_or_404(Staff, user_id=request.user.id)

    query = (request.GET.get("search") or "").strip()
    appointments = _get_staff_appointments_by_search(staff.staff_id, query)

    return render(request, "appointments/staff_my_appointments.html", {
        "appointments": appointments,
        "search_query": query,
    })

def get_staffs_by_search(query):
    sql = "SELECT * FROM staff "
    params = []
    if query:
        sql += (
            " WHERE first_name LIKE %s "
            "OR last_name LIKE %s "
            "OR phone LIKE %s "
            "OR email LIKE %s "
            "OR specialty LIKE %s "
            "OR position LIKE %s "
        )
        search = f"%{query}%"
        params = [search] * 6
    sql += "ORDER BY is_active DESC, commission_rate DESC "
    return Staff.objects.raw(sql, params)

def get_favorite_staff():
    sql = """
            SELECT staff.staff_id, first_name, last_name, COUNT(*) AS appointments
            FROM appointment, staff
            WHERE appointment.staff_id = staff.staff_id
            GROUP BY staff_id
            HAVING COUNT(*) = (
            SELECT MAX(appointment_count)
            FROM (SELECT COUNT(*) AS appointment_count
            FROM appointment
            GROUP BY staff_id
            ) AS counts
            )
            LIMIT 5
        """
    return Staff.objects.raw(sql)

def get_positive_staff():
    sql = """
        SELECT staff.staff_id, first_name, last_name, COUNT(*) AS five_star_reviews
        FROM review, staff
        WHERE rating = 5
        AND review.staff_id = staff.staff_id
        GROUP BY staff_id
        HAVING COUNT(*) = (
            SELECT MAX(staff_review_count)
            FROM (
                SELECT COUNT(*) AS staff_review_count
                FROM review
                WHERE rating = 5
                GROUP BY staff_id
            ) AS counts
        )
        LIMIT 1
    """
    return Staff.objects.raw(sql)

def get_employee_of_the_month(year, month):
    sql = """
        SELECT s.staff_id, s.first_name, s.last_name, SUM(p.amount) AS contribution
        FROM staff s, appointment a, payment p
        WHERE s.staff_id = a.staff_id
        AND a.appointment_id = p.appointment_id
        
        AND YEAR(a.appointment_date) = %s AND MONTH(a.appointment_date) = %s
        AND a.status = 'completed'
        GROUP BY s.staff_id
        ORDER BY contribution DESC
        LIMIT 1
    """
    params = [year, month]
    return Staff.objects.raw(sql, params)

def staff_list(request):
    query = request.GET.get('search', '').strip()

    favorite_staffs = request.GET.get('favorite_staffs')
    positive_staffs = request.GET.get('positive_staffs')

    staffs = get_staffs_by_search(query)

    selected_date = request.GET.get('date')
    if not selected_date:
        selected_date = date.today().isoformat()  # e.g., '2025-08-09'
    employee_of_the_month = request.GET.get('employee_of_the_month')


    if favorite_staffs:
        staffs = get_favorite_staff()
    elif positive_staffs:
        staffs = get_positive_staff()
    elif employee_of_the_month and selected_date:
        try:
            year, month = selected_date[:7].split('-')
            staffs = get_employee_of_the_month(year, month)
        except ValueError:
            staffs = []
    else:
        staffs = get_staffs_by_search(query)

    return render(request, 'staffs/staffs.html', {
        'staffs': staffs,
        'selected_date': selected_date,
        'search_query': query,
    })


def staff_add(request):
    if request.method == 'POST':
        data = request.POST

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO staff
                (first_name, last_name, phone, email, hire_date, position,
                 commission_rate, specialty, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    data['first_name'],
                    data['last_name'],
                    data['phone'],
                    data.get('email') or None,
                    data['hire_date'],
                    data['position'],
                    data.get('commission_rate') or 0.15,
                    data.get('specialty') or None,
                    data.get('is_active') or 1,
                ]
            )
            staff_id = cursor.lastrowid

        # create auth_user and link
        username = (data.get('username') or '').strip()
        password = (data.get('password') or '').strip()
        if username and password:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data.get('email') or '',
                is_staff=True,   
                is_active=True,
            )
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE staff SET user_id = %s WHERE staff_id = %s",
                    [user.id, staff_id]
                )

        return redirect('staff_list')

    return render(request, 'staffs/staff_add.html')


def staff_edit(request, staff_id):
    # Load STAFF + linked auth user (username)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                s.staff_id,
                s.first_name,
                s.last_name,
                s.phone,
                s.email,
                s.hire_date,
                s.position,
                s.commission_rate,
                s.specialty,
                s.is_active,
                s.user_id,
                u.username
            FROM staff s
            LEFT JOIN auth_user u ON u.id = s.user_id
            WHERE s.staff_id = %s
        """, [staff_id])
        row = cursor.fetchone()

    if not row:
        return render(request, '404.html')

    staff = {
        'staff_id': row[0],
        'first_name': row[1],
        'last_name': row[2],
        'phone': row[3],
        'email': row[4],
        'hire_date': row[5],  # template formats to Y-m-d
        'position': row[6],
        'commission_rate': row[7],
        'specialty': row[8] or '',
        'is_active': bool(row[9]),
        'user_id': row[10],
        'username': row[11] or '',
    }

    if request.method == 'POST':
        data = request.POST

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE staff
                SET first_name=%s, last_name=%s, phone=%s, email=%s,
                    hire_date=%s, position=%s, commission_rate=%s,
                    specialty=%s, is_active=%s
                WHERE staff_id=%s
                """,
                [
                    data['first_name'],
                    data['last_name'],
                    data['phone'],
                    data.get('email') or None,
                    data['hire_date'],
                    data['position'],
                    data.get('commission_rate') or 0.15,
                    data.get('specialty') or None,
                    data.get('is_active') or 1,
                    staff_id
                ]
            )

        #  Sync / create auth_user
        new_username = (data.get('username') or '').strip()
        new_password = (data.get('password') or '').strip()

        first_name = data['first_name']
        last_name  = data['last_name']
        email      = data.get('email') or ''

        try:
            if staff['user_id']:
                user = User.objects.get(pk=staff['user_id'])

                if new_username:
                    user.username = new_username  
                user.first_name = first_name
                user.last_name  = last_name
                user.email      = email
                user.is_staff   = True
                user.is_active  = True

                if new_password:
                    user.set_password(new_password)

                user.save()
            else:
                if new_username and new_password:
                    user = User.objects.create_user(
                        username=new_username,
                        password=new_password,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        is_staff=True,
                        is_active=True,
                    )
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE staff SET user_id = %s WHERE staff_id = %s",
                            [user.id, staff_id]
                        )

        except IntegrityError:
            # Re-render with error and current inputs
            staff.update({
                'first_name': first_name,
                'last_name': last_name,
                'phone': data['phone'],
                'email': email,
                'hire_date': data['hire_date'],
                'position': data['position'],
                'commission_rate': data.get('commission_rate') or 0.15,
                'specialty': data.get('specialty') or '',
                'is_active': bool(int(data.get('is_active') or 1)),
                'username': new_username,
            })
            return render(request, 'staffs/staff_edit.html', {
                'staff': staff,
                'error': 'That username is already taken. Please choose a different one.',
            })

        return redirect('staff_list')

    return render(request, 'staffs/staff_edit.html', {'staff': staff})

def staff_delete(request, staff_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM staff WHERE staff_id=%s", [staff_id])
        return redirect('staff_list')
    return redirect('staff_list') 
