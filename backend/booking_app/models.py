import uuid
from auth_app.models import Vehicle, Servicing
from django.db import models
from django.conf import settings

# Create your models here.
class ServiceBooking(models.Model):
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    booking_id = models.UUIDField(primary_key=True, unique=True, null=False, editable=False ,default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    service = models.ForeignKey(Servicing, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)

    def __str__(self):
        return f"Service booking for {self.user.username if self.user else 'Unknown'} on {self.date} at {self.time}"


class VehicleBooking(models.Model):
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    booking_id = models.UUIDField(primary_key=True, unique=True, null=False, editable=False ,default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Associated Vehicle")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Vehicle purchase booking for {self.user.username if self.user else 'Unknown'} on {self.date} at {self.time}"
