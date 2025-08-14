from django.urls import path
from . import (views, views_customer, views_staff, views_event, views_inventory, 
               views_service, views_appointment, views_my_appointment, views_payment, 
               views_guest_appointment, views_review)

urlpatterns = [
    path('', views.views_main, name='main'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Staff paths
    path('staffs/', views_staff.staff_list, name='staff_list'),
    path('staffs/add/', views_staff.staff_add, name='staff_add'),
    path('staffs/<int:staff_id>/edit/', views_staff.staff_edit, name='staff_edit'),
    path('staffs/<int:staff_id>/delete/', views_staff.staff_delete, name='staff_delete'),

    # Customer paths
    path('customers/', views_customer.customer_list, name='customer_list'),
    path('customers/add/', views_customer.customer_add, name='customer_add'),
    path('customers/<int:customer_id>/edit/', views_customer.customer_edit, name='customer_edit'),
    path('customers/<int:customer_id>/delete/', views_customer.customer_delete, name='customer_delete'),

    # Event paths
    path('events/', views_event.event_list, name='event_list'),
    path('events/add/', views_event.event_add, name='event_add'),
    path('events/<int:events_id>/edit/', views_event.event_edit, name='event_edit'),
    path('events/<int:events_id>/delete/', views_event.event_delete, name='event_delete'),

    # Inventory paths
    path('inventory/', views_inventory.inventory_list, name='inventory_list'),
    path('inventory/add/', views_inventory.inventory_add, name='inventory_add'),
    path('inventory/<int:inventory_id>/edit/', views_inventory.inventory_edit, name='inventory_edit'),
    path('inventory/<int:inventory_id>/delete/', views_inventory.inventory_delete, name='inventory_delete'),

    # Service paths
    path('services/', views_service.service_list, name='service_list'),
    path('services/add/', views_service.service_add, name='service_add'),
    path('services/<int:service_id>/edit/', views_service.service_edit, name='service_edit'),
    path('services/<int:service_id>/delete/', views_service.service_delete, name='service_delete'),

    # Appointment paths
    path('appointments/', views_appointment.appointment_list, name='appointment_list'),
    path('appointments/add/', views_appointment.appointment_add, name='appointment_add'),
    path('appointments/<int:appointment_id>/edit/', views_appointment.appointment_edit, name='appointment_edit'),
    path('appointments/<int:appointment_id>/delete/', views_appointment.appointment_delete, name='appointment_delete'),
    path('<int:appointment_id>/finish/', views_appointment.appointment_finish, name='appointment_finish'),
    path('my_appointments/', views_my_appointment.my_appointment_list, name='my_appointments'),
    path('my_appointments/add/', views_my_appointment.my_appointment_add, name='my_appointment_add'),
    path('my_appointments/<int:appointment_id>/edit/', views_my_appointment.my_appointment_edit, name='my_appointment_edit'),
    #path('guest_appointments/', views_guest_appointment.guest_appointment_add, name='guest_appointments_add'),

    # payment paths
    path('payments/', views_payment.payment_list, name='payment_list'),
    path('payments/add/', views_payment.payment_add, name='payment_add'),
    path('payments/<int:payment_id>/edit/', views_payment.payment_edit, name='payment_edit'),
    path('payments/<int:payment_id>/delete/', views_payment.payment_delete, name='payment_delete'),

    # Review paths
    path('reviews/', views_review.reviews_list, name='reviews_list'),
    path('reviews/add/', views_review.review_add, name='review_add'),
    path('reviews/<int:review_id>/edit/', views_review.review_edit, name='review_edit'),
    path('reviews/<int:review_id>/delete/', views_review.review_delete, name='review_delete'),
    # NEW (customer review add/edit)
    path('my_reviews/<int:appointment_id>/review/add/', views_my_appointment.my_review_add, name='my_review_add'),
    path('my_reviews/<int:review_id>/edit/', views_my_appointment.my_review_edit, name='my_review_edit'),
]