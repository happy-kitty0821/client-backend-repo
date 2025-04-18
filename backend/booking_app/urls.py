from django.urls import path
from .views import *

urlpatterns = [
    path('book-vehicle/', BookVehicleAPIView.as_view(), name='book-vehicle'),
     path('vehicle-booking/<uuid:booking_id>/update-status/', UpdateVehicleBookingStatusView.as_view(), name='vehicle-booking-update-status'),
    #services urls
    path('book-service/', BookServiceAPIView.as_view(), name='book-vehicle'),
    path('service-booking/<uuid:booking_id>/update-status/', UpdateServiceBookingStatusView.as_view(), name='service-booking-update-status'),
    #user's booking
    path('user/bookings/', GetUserBookings.as_view(), name='get_user_bookings'),

]
