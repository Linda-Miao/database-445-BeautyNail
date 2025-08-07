from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff
from django.db import connection
from datetime import date
from django.contrib import messages

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
        LIMIT 5
    """
    return Staff.objects.raw(sql)

def get_employee_of_the_month(year, month):
    sql = """
        SELECT staff.staff_id, staff.first_name, staff.last_name, SUM(payment.amount + payment.tip_amount) AS contribution
        FROM staff
        JOIN appointment ON appointment.staff_id = staff.staff_id
        JOIN payment ON payment.appointment_id = appointment.appointment_id
        WHERE YEAR(appointment.appointment_date) = %s AND MONTH(appointment.appointment_date) = %s
        GROUP BY staff.staff_id
        ORDER BY contribution DESC
        LIMIT 5
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
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip() or None
        hire_date = request.POST.get('hire_date')  # 'YYYY-MM-DD'
        position = request.POST.get('position', '').strip()
        commission_rate = request.POST.get('commission_rate')  # string -> Decimal ok
        specialty = request.POST.get('specialty', '').strip() or None
        is_active = request.POST.get('is_active') == '1'

        Staff.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            hire_date=hire_date,
            position=position,
            commission_rate=commission_rate,
            specialty=specialty,
            is_active=is_active,
        )
        messages.success(request, 'Staff member added.')
        return redirect('staff_list')

    return render(request, 'staffs/staff_add.html')

def staff_edit(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)

    if request.method == 'POST':
        staff.first_name = request.POST.get('first_name', '').strip()
        staff.last_name = request.POST.get('last_name', '').strip()
        staff.phone = request.POST.get('phone', '').strip()
        staff.email = (request.POST.get('email', '').strip() or None)
        staff.hire_date = request.POST.get('hire_date')  # 'YYYY-MM-DD'
        staff.position = request.POST.get('position', '').strip()
        staff.commission_rate = request.POST.get('commission_rate')
        staff.specialty = (request.POST.get('specialty', '').strip() or None)
        staff.is_active = (request.POST.get('is_active') == '1')

        staff.save()
        messages.success(request, 'Staff member updated.')
        return redirect('staff_list')

    return render(request, 'staffs/staff_edit.html', {'staff': staff})

def staff_delete(request, staff_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM staff WHERE staff_id=%s", [staff_id])
        return redirect('staff_list')
    return redirect('staff_list') 
