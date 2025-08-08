# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', models.DO_NOTHING)
    staff = models.ForeignKey('Staff', models.DO_NOTHING)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment'


class AppointmentService(models.Model):
    appointment_service_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, models.DO_NOTHING)
    service = models.ForeignKey('Service', models.DO_NOTHING)
    service_price = models.DecimalField(max_digits=8, decimal_places=2)
    polish_color = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment_service'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    preferred_color = models.CharField(max_length=50, blank=True, null=True)
    loyalty_points = models.IntegerField(blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50)
    color_name = models.CharField(max_length=50, blank=True, null=True)
    quantity_in_stock = models.IntegerField(blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=6, decimal_places=2)
    retail_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    reorder_level = models.IntegerField(blank=True, null=True)
    supplier_name = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, models.DO_NOTHING)
    payment_method = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    tip_amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment'


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    appointment = models.ForeignKey(Appointment, models.DO_NOTHING)
    staff = models.ForeignKey('Staff', models.DO_NOTHING)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_minutes = models.IntegerField()
    category = models.CharField(max_length=50)
    requies_appointment = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service'


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    hire_date = models.DateField()
    position = models.CharField(max_length=50)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    specialty = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff'

class Event(models.Model):
    events_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    # NOTE: the DB column is "decription" (typo). Map it explicitly:
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'EVENTS'
        managed = False

    def __str__(self):
        return self.event_name

