from rest_framework import generics
from .models import VehicleBooking
from .serializers import *
from .permissions import IsCustomer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from itertools import chain
from operator import attrgetter


class BookVehicleAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, *args, **kwargs):
        serializer = VehicleBookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            booking = serializer.save()
            return Response({
                "message": "Vehicle booked successfully!",
                "data": VehicleBookingSerializer(booking).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateVehicleBookingStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, booking_id):
        try:
            booking = VehicleBooking.objects.get(booking_id=booking_id, user=request.user)
        except VehicleBooking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = VehicleBookingStatusUpdateSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": f"Vehicle booking status updated to {serializer.validated_data['status']}.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookServiceAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, *args, **kwargs):
        serializer = ServicingBookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            booking = serializer.save()
            return Response({
                "message": "Servicing booked successfully!",
                "data": ServicingBookingSerializer(booking, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateServiceBookingStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, booking_id):
        try:
            booking = ServiceBooking.objects.get(booking_id=booking_id, user=request.user)
        except ServiceBooking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=http_status.HTTP_404_NOT_FOUND)

        serializer = ServiceBookingStatusUpdateSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": f"Service booking status updated to {serializer.validated_data.get('status', 'unknown')}.",
                "data": serializer.data
            }, status=http_status.HTTP_200_OK)

        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
    
#fetch user's booking weather it is service or vehicel
class GetUserBookings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        vehicle_bookings = VehicleBooking.objects.filter(user=user)
        service_bookings = ServiceBooking.objects.filter(user=user)

        # Add type field manually
        for vb in vehicle_bookings:
            vb.type = "Vehicle Purchase"
        for sb in service_bookings:
            sb.type = "Vehicle Service Booking"

        # Combine both querysets
        combined = sorted(
            chain(vehicle_bookings, service_bookings),
            key=attrgetter('created_at'),
            reverse=True
        )

        serializer = GetUserBookingsSerializer(combined, many=True)
        return Response(serializer.data)