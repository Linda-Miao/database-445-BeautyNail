from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Customer,Review,Staff
from django.db import connection, IntegrityError
from django.contrib.auth.models import User


# Django support insert, edit, delete using ORM so we only implement the insert, edit, delete function using raw query only for customer table
def customer_add(request):
    if request.method == 'POST':
        data = request.POST

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO customer 
                (first_name, last_name, phone, email, date_of_birth, allergies, preferred_color, loyalty_points, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    data['first_name'],
                    data['last_name'],
                    data['phone'],
                    data.get('email') or None,
                    data.get('date_of_birth') or None,
                    data.get('allergies') or None,
                    data.get('preferred_color') or None,
                    data.get('loyalty_points') or 0,
                    data.get('is_active') or 1
                ]
            )
            customer_id = cursor.lastrowid  # new customer ID

        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data.get('email') or ''
            )

            # Link the created user to the customer
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE customer SET user_id = %s WHERE customer_id = %s",
                    [user.id, customer_id]
                )

        return redirect('customer_list')

    return render(request, 'customers/customer_add.html')

def customer_edit(request, customer_id):
    # Load customer + linked auth user info
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                c.customer_id,
                c.first_name,
                c.last_name,
                c.phone,
                c.email,
                c.date_of_birth,
                c.allergies,
                c.preferred_color,
                c.loyalty_points,
                c.registration_date,
                c.is_active,
                c.user_id,
                u.username
            FROM customer c
            LEFT JOIN auth_user u ON u.id = c.user_id
            WHERE c.customer_id = %s
        """, [customer_id])
        row = cursor.fetchone()

    if not row:
        return render(request, '404.html')

    cust = {
        'customer_id': row[0],
        'first_name': row[1],
        'last_name': row[2],
        'phone': row[3],
        'email': row[4],
        'date_of_birth': row[5].isoformat() if row[5] else '',
        'allergies': row[6] or '',
        'preferred_color': row[7] or '',
        'loyalty_points': row[8],
        'registration_date': row[9],
        'is_active': bool(row[10]),
        'user_id': row[11],
        'username': row[12] or '',
    }

    if request.method == 'POST':
        data = request.POST

        # 1) Update the CUSTOMER row 
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE customer
                SET first_name=%s, last_name=%s, phone=%s, email=%s,
                    date_of_birth=%s, allergies=%s, preferred_color=%s,
                    loyalty_points=%s, is_active=%s
                WHERE customer_id=%s
                """,
                [
                    data['first_name'],
                    data['last_name'],
                    data['phone'],
                    data.get('email') or None,
                    data.get('date_of_birth') or None,
                    data.get('allergies') or None,
                    data.get('preferred_color') or None,
                    data.get('loyalty_points') or 0,
                    data.get('is_active') or 1,
                    customer_id
                ]
            )

        # 2) Sync / create the auth user if requested
        new_username = (data.get('username') or '').strip()
        new_password = (data.get('password') or '').strip()

        # Refresh cust fields for syncing with auth_user
        first_name = data['first_name']
        last_name  = data['last_name']
        email      = data.get('email') or ''

        try:
            if cust['user_id']:
                # Linked user exists — update if username provided or password provided
                user = User.objects.get(pk=cust['user_id'])

                if new_username:
                    user.username = new_username
                # Always keep names/email in sync with CUSTOMER edits
                user.first_name = first_name
                user.last_name  = last_name
                user.email      = email

                if new_password:
                    user.set_password(new_password)

                user.save()

            else:
                # No linked user — if both username and password provided, create and link
                if new_username and new_password:
                    user = User.objects.create_user(
                        username=new_username,
                        password=new_password,
                        first_name=first_name,
                        last_name=last_name,
                        email=email
                    )
                    # Link this new user to the customer
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE customer SET user_id = %s WHERE customer_id = %s",
                            [user.id, customer_id]
                        )
                # If only one of username/password is provided, ignore creating user (silent)

        except IntegrityError:
            # Username already taken (or other unique violation)
            # Re-render form with error and current user-entered fields
            cust.update({
                'first_name': first_name,
                'last_name': last_name,
                'phone': data['phone'],
                'email': email,
                'date_of_birth': data.get('date_of_birth') or '',
                'allergies': data.get('allergies') or '',
                'preferred_color': data.get('preferred_color') or '',
                'loyalty_points': data.get('loyalty_points') or 0,
                'is_active': bool(int(data.get('is_active') or 1)),
                'username': new_username,
            })
            return render(request, 'customers/customer_edit.html', {
                'customer': cust,
                'error': 'That username is already taken. Please choose a different one.',
            })

        return redirect('customer_list')

    # GET
    return render(request, 'customers/customer_edit.html', {'customer': cust})

def customer_delete(request, customer_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM customer WHERE customer_id=%s", [customer_id])
        return redirect('customer_list')
    return redirect('customer_list') 


def get_customers_by_search(query):
    sql = "SELECT * FROM customer"
    params = []
    if query:
        sql += " WHERE first_name LIKE %s OR last_name LIKE %s OR phone LIKE %s OR email LIKE %s "
        search = f"%{query}%"
        params = [search] * 4
    sql += " ORDER BY is_active DESC, loyalty_points DESC "
    return Customer.objects.raw(sql, params)

def get_top_customers():
    sql = """
        SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount + p.tip_amount) AS total_payment
        FROM customer as c, appointment as a, payment as p
        WHERE c.customer_id = a.customer_id
        AND a.appointment_id = p.appointment_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        HAVING SUM(p.amount + p.tip_amount) = (
            SELECT MAX(total_amount) FROM (
                SELECT SUM(p1.amount + p1.tip_amount) AS total_amount
                FROM appointment as a1, payment as p1
                WHERE a1.appointment_id = p1.appointment_id
                GROUP BY a1.customer_id
            ) AS totals
        )
    """
    return Customer.objects.raw(sql)

def get_negative_reviewers():
    sql = """
        SELECT 
               r.review_id,       
               r.rating,
               c.customer_id, c.first_name, c.last_name, c.phone, c.email, c.loyalty_points,
               r.appointment_id,
               s.first_name AS staff_first_name, s.last_name AS staff_last_name
        FROM review AS r, customer AS c, staff AS s
        WHERE  r.customer_id = c.customer_id
        AND  r.staff_id = s.staff_id
        AND r.rating < 3
        ORDER BY r.rating ASC
    """
    return Customer.objects.raw(sql)

def customer_list(request):
    query = request.GET.get('search', '').strip()
    top_customer = request.GET.get('top_customer')
    unsatisfy_customer = request.GET.get('unsatisfy_customer')

    if top_customer:
        customers = get_top_customers()
    elif unsatisfy_customer:
        customers = get_negative_reviewers()
    else:
        customers = get_customers_by_search(query)

    return render(request, 'customers/customers.html', {
        'customers': customers,
        'search_query': query
    })