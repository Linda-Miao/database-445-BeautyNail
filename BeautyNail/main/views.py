from django.shortcuts import render, redirect	
from django.contrib import messages
from django.http import HttpResponse
from .models import Customer, Review, Staff, Service
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.

def _popular_services(limit=4):
    sql = """
        SELECT
            s.service_id,              
            s.service_name,
            s.description,
            s.base_price,
            COUNT(*) AS usage_count
        FROM APPOINTMENT_SERVICE aps
        JOIN SERVICE s ON aps.service_id = s.service_id
        GROUP BY s.service_id, s.service_name, s.description, s.base_price
        ORDER BY usage_count DESC, s.service_name ASC
        LIMIT %s
    """
    return list(Service.objects.raw(sql, [limit]))

def _top_testimonials(limit=6):
    sql = """
        SELECT
            r.review_id,                                   -- pk required by Django raw()
            CONCAT(c.first_name, ' ', c.last_name) AS author_name,
            r.comment,
            r.rating,
            (
              SELECT s.service_name
              FROM APPOINTMENT a2
              JOIN APPOINTMENT_SERVICE aps ON aps.appointment_id = a2.appointment_id
              JOIN SERVICE s ON s.service_id = aps.service_id
              WHERE a2.appointment_id = r.appointment_id
              LIMIT 1
            ) AS service_name
        FROM REVIEW r, CUSTOMER c
        WHERE c.customer_id = r.customer_id
        AND r.comment IS NOT NULL AND r.comment <> ''
        ORDER BY r.rating DESC, r.review_id DESC
        LIMIT %s
    """
    return list(Review.objects.raw(sql, [limit]))

def customer_reviews(request):
    # Pass dynamic reviews if available; template falls back to static samples if empty
    reviews = _top_testimonials(6)
    return render(request, 'customer_reviews.html', {'reviews': reviews})

def home(request):
    popular_services = _popular_services(4)
    return render(request, 'home.html', {'popular_services': popular_services})

def views_project_page(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM customer")
        customers_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM appointment")
        appointments_count = cursor.fetchone()[0]

    return render(request, 'project_page.html', {
        'customers_count': customers_count,
        'appointments_count': appointments_count,
    })

def services_all(request):
    services = Service.objects.all().order_by('service_name')
    return render(request, 'service_home.html', {'services': services})

def views_about(request):
        return render(request, 'about.html', )

def user_login(request):
    if request.method == 'POST':
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Go to home page
        else:
            messages.error(request, 'Invalid username or password',xtra_tags="login_error")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Back to login page