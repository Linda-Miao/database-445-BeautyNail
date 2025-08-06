from django.contrib import admin

# Register your models here.
from .models import Customer, Appointment, Service, Staff, Payment, Review, Inventory, AppointmentService

admin.site.register(Customer)
admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(Staff)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Inventory)
admin.site.register(AppointmentService)
