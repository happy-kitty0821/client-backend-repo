import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('service_manager', 'Service Manager'),
        ('customer', 'Customer'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.set_password(self.password)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

# Service Center Model
class ServiceCenter(models.Model):
    center_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    location = models.TextField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    center_manager = models.OneToOneField("User", on_delete=models.PROTECT)
    center_logo = models.ImageField(upload_to='service_center_logo/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} managed by {self.center_manager.username}"

# Vehicle Model
class Vehicle(models.Model):
    vehicle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    vin = models.CharField(max_length=17, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="vehicle_images/", blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sold_by = models.ForeignKey("ServiceCenter", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

# Servicing Model
class Servicing(models.Model):
    service_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    provided_by = models.ForeignKey("ServiceCenter", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} by {self.provided_by.name}" 


