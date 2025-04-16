from django.contrib import admin
from .models import User, ServiceCenter, Vehicle, Servicing

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone_number', 'city', 'country')
    list_filter = ('role', 'city', 'country')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(ServiceCenter)
class ServiceCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'open_time', 'close_time', 'center_manager')
    search_fields = ('name', 'location', 'center_manager__username')
    list_filter = ('open_time', 'close_time')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'vin', 'price', 'discount', 'sold_by')
    search_fields = ('make', 'model', 'vin')
    list_filter = ('year', 'make', 'sold_by')

@admin.register(Servicing)
class ServicingAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'discount', 'provided_by')
    search_fields = ('name', 'provided_by__name')
    list_filter = ('provided_by',)
