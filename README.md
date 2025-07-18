# database-445-BeautyNail

445-database course project



-Using virtualenv

-Install Django: pip install Django

-create Django project: django-admin startproject BeautyNail

-Go to BeautyNail folder: python manage.py runserver

-Setup MySQL or django: https://dev.to/sm0ke/how-to-use-mysql-with-django-for-beginners-2ni0

-Create tables : python manage.py makemigrations

 		 python manage.py migrate



-Steps to create first page: 

&nbsp;	.In project root folder (where manage.py is): python manage.py startapp main

&nbsp;	.open settings.py and add 'main', to INSTALLED\_APPS:

&nbsp;	.Inside main/models.py, add:

&nbsp;		from django.db import models



&nbsp;		class Customer(models.Model):
			customer_id = models.AutoField(primary_key=True)  # 👈 tell Django this is the primary key

&nbsp;   		first\_name = models.CharField(max\_length=50)

&nbsp;   		last\_name = models.CharField(max\_length=50)

&nbsp;   		phone = models.CharField(max\_length=15)

&nbsp;   		email = models.CharField(max\_length=100, null=True, blank=True)

&nbsp;   		date\_of\_birth = models.DateField(null=True, blank=True)

&nbsp;   		allergies = models.TextField(null=True, blank=True)

&nbsp;   		preferred\_color = models.CharField(max\_length=50, null=True, blank=True)

&nbsp;   		loyalty\_points = models.IntegerField(default=0)

&nbsp;   		registration\_date = models.DateField(null=True, blank=True)

&nbsp;   		is\_active = models.BooleanField(default=True)



&nbsp;   		def \_\_str\_\_(self):

&nbsp;       	return f"{self.first\_name} {self.last\_name}"

&nbsp;			class Meta:

&nbsp;       		db\_table = 'CUSTOMER'  # match your MySQL table

&nbsp;       		managed = False        # tell Django not to try to create it
	.Create a "templates" folder in main
	.Create a template html file "main.html"
		<!DOCTYPE html>
		<html>
		<head>
    		<title>Hello Page</title>
		</head>
		<body>
    		<h1>Hello</h1>

    		<h2>Top 2 Customers:</h2>
    		<ul>
        	{% for customer in customers %}
            		<li>{{ customer.first_name }} {{ customer.last_name }} ({{ customer.phone }})</li>
        	{% empty %}
            		<li>No customers found.</li>
        	{% endfor %}
    		</ul>

    			<a href="{% url 'about' %}">Go to About Page</a>
		</body>
		</html>

&nbsp;	.Create a Simple View in main/views.py

		from django.shortcuts import render
		from .models import Customer

		def hello_customers(request):
    		customers = Customer.objects.all()[:2]
    		return render(request, 'main.html', {'customers': customers})


	.In main/urls add this:
		from django.urls import path
		from . import views

		urlpatterns = [
    			path('', views.hello_customers, name='main'),
		]

	.In urls of main project add this in urlpatterns:
		urlpatterns = [
    			path('', include('main.urls')),  # include main.urls here
		]

	