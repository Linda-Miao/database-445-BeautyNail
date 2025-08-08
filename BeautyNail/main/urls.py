from django.urls import path
from . import views, views_customer, views_staff, views_event

urlpatterns = [
    path('', views.views_main, name='main'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('staffs/', views_staff.staff_list, name='staff_list'),
    path('staffs/add/', views_staff.staff_add, name='staff_add'),
    path('staffs/<int:staff_id>/edit/', views_staff.staff_edit, name='staff_edit'),
    path('staffs/<int:staff_id>/delete/', views_staff.staff_delete, name='staff_delete'),
    path('customers/', views_customer.customer_list, name='customer_list'),
    path('customers/add/', views_customer.customer_add, name='customer_add'),
    path('customers/<int:customer_id>/edit/', views_customer.customer_edit, name='customer_edit'),
    path('customers/<int:customer_id>/delete/', views_customer.customer_delete, name='customer_delete'),
    path('events/', views_event.event_list, name='event_list'),
    path('events/add/', views_event.event_add, name='event_add'),
    path('events/<int:events_id>/edit/', views_event.event_edit, name='event_edit'),
    path('events/<int:events_id>/delete/', views_event.event_delete, name='event_delete'),
]