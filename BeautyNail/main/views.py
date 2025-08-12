from django.shortcuts import render, redirect	
from django.contrib import messages
from django.http import HttpResponse
from .models import Customer,Review,Staff
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.


def views_main(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM customer")
        customers_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM appointment")
        appointments_count = cursor.fetchone()[0]

    return render(request, 'main.html', {
        'customers_count': customers_count,
        'appointments_count': appointments_count,
    })

def views_about(request):
        return render(request, 'about.html', )

def user_login(request):
    if request.method == 'POST':
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('main')  # Go to home page
        else:
            messages.error(request, 'Invalid username or password',xtra_tags="login_error")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Back to login page