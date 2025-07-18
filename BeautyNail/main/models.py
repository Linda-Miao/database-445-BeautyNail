from django.db import models

# Create your models here.

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)  # 👈 tell Django this is the primary key
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
        db_table = 'CUSTOMER'  # match MySQL table
        managed = False        # tell Django not to try to create it