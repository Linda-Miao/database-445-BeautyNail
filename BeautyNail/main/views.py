from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Customer,Review,Staff
from django.db import connection
# Create your views here.


def hello_customers(request):
    	customers = Customer.objects.all()[:2]
    	return render(request, 'main.html', {'customers': customers})

def views_about(request):
        return render(request, 'about.html', )
