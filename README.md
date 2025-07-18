
# 💅 BeautyNail — 445 Database Course Project

This is a Django + MySQL web project for the 445 Database course.

---

## ⚙️ Setup Instructions

### ✅ 1. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### ✅ 2. Install Django

```bash
pip install Django
```

### ✅ 3. Start the Django Project

```bash
django-admin startproject BeautyNail
cd BeautyNail
```

Run the server to test:

```bash
python manage.py runserver
```

---

## 🛠️ Connect Django to MySQL

Follow this guide to set up MySQL with Django:  
📎 [How to Use MySQL with Django (dev.to)](https://dev.to/sm0ke/how-to-use-mysql-with-django-for-beginners-2ni0)

---

## 🧱 Create Database Tables

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🧪 Create First Page to Display Customers

### ✅ Step 1: Start a Django App

```bash
python manage.py startapp main
```

### ✅ Step 2: Register App in `settings.py`

Add `'main',` to `INSTALLED_APPS`.

---

### ✅ Step 3: Define the `Customer` Model in `main/models.py`

```python
from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    preferred_color = models.CharField(max_length=50, null=True, blank=True)
    loyalty_points = models.IntegerField(default=0)
    registration_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'CUSTOMER'
        managed = False
```

---

### ✅ Step 4: Create a Template

1. Inside the `main/` app, create a folder named: `templates/main/`
2. Create a file `hello.html` inside it.

#### `main/templates/main/hello.html`

```html
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
```

---

### ✅ Step 5: Create a View in `main/views.py`

```python
from django.shortcuts import render
from .models import Customer

def hello_customers(request):
    customers = Customer.objects.all()[:2]
    return render(request, 'main/hello.html', {'customers': customers})
```

---

### ✅ Step 6: Add URL Pattern in `main/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_customers, name='main'),
]
```

---

### ✅ Step 7: Include App URLs in `BeautyNail/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
```

---

## ✅ You're Done!

Now run the server:

```bash
python manage.py runserver
```

Then visit:  
http://127.0.0.1:8000/  
You should see a "Hello" heading and the top 2 customers from your database.
