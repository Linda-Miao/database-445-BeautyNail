from django.urls import path
from . import views, views_customer, views_staff

urlpatterns = [
    path('', views.hello_customers, name='main'),
    path('about', views.views_about, name='about'),
    path('staffs/', views_staff.staff_list, name='staff_list'),
    path('staffs/add/', views_staff.staff_add, name='staff_add'),
    path('staffs/<int:staff_id>/edit/', views_staff.staff_edit, name='staff_edit'),
    path('staffs/<int:staff_id>/delete/', views_staff.staff_delete, name='staff_delete'),
    path('customers/', views_customer.customer_list, name='customer_list'),
    path('customers/add/', views_customer.customer_add, name='customer_add'),
    path('customers/<int:customer_id>/edit/', views_customer.customer_edit, name='customer_edit'),
    path('customers/<int:customer_id>/delete/', views_customer.customer_delete, name='customer_delete'),
]