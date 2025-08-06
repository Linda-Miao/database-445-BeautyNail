from django.db import models

# Create your models here.

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    hire_date = models.DateField()
    position = models.CharField(max_length=50)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.15)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'STAFF'
        managed = False


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_minutes = models.IntegerField()
    category = models.CharField(max_length=50)
    requies_appointment = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name

    class Meta:
        db_table = 'SERVICE'
        managed = False


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=50)
    color_name = models.CharField(max_length=50, null=True, blank=True)
    quantity_in_stock = models.IntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=6, decimal_places=2)
    retail_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    reorder_level = models.IntegerField(default=5)
    supplier_name = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'INVENTORY'
        managed = False


class Events(models.Model):
    events_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    decription = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = 'EVENTS'
        managed = False


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.RESTRICT, db_column='customer_id')
    staff = models.ForeignKey('Staff', on_delete=models.RESTRICT, db_column='staff_id')
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='scheduled')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment {self.appointment_id}"

    class Meta:
        db_table = 'APPOINTMENT'
        managed = False


class AppointmentService(models.Model):
    appointment_service_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, db_column='appointment_id')
    service = models.ForeignKey('Service', on_delete=models.RESTRICT, db_column='service_id')
    service_price = models.DecimalField(max_digits=8, decimal_places=2)
    polish_color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Appointment Service {self.appointment_service_id}"

    class Meta:
        db_table = 'APPOINTMENT_SERVICE'
        managed = False


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, db_column='appointment_id')
    payment_method = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    tip_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Payment {self.payment_id}"

    class Meta:
        db_table = 'PAYMENT'
        managed = False


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.RESTRICT, db_column='customer_id')
    appointment = models.ForeignKey('Appointment', on_delete=models.RESTRICT, db_column='appointment_id')
    staff = models.ForeignKey('Staff', on_delete=models.RESTRICT, db_column='staff_id')
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.review_id} by {self.customer}"

    class Meta:
        db_table = 'REVIEW'
        managed = False
