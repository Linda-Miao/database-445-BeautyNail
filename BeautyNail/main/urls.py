from django.urls import path
from . import views, views_customer

urlpatterns = [
    path('', views.hello_customers, name='main'),
    path('about', views.views_about, name='about'),
    path('customers/', views_customer.customer_list, name='customer_list'),
    path('customers/add/', views_customer.customer_add, name='customer_add'),
    path('customers/<int:customer_id>/edit/', views_customer.customer_edit, name='customer_edit'),
    path('customers/<int:customer_id>/delete/', views_customer.customer_delete, name='customer_delete'),
]