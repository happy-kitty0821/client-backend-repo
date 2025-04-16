from django.contrib import admin
from .models import ServiceBooking, VehicleBooking

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'service', 'status', 'date', 'time', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'service__name')
    ordering = ('-created_at',)


@admin.register(VehicleBooking)
class VehicleBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'vehicle', 'total_price', 'status', 'date', 'time', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'vehicle__make', 'vehicle__model')
    ordering = ('-created_at',)
