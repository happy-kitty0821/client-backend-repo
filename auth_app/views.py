from django.http import JsonResponse
from rest_framework import generics, permissions, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .permissions import *
from rest_framework.exceptions import PermissionDenied
from rest_framework import status



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        update_last_login(None, user)
        
        response = Response({
            "id" : user.id,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user.username,
            "role": user.role,
            "message": "Login successful"
        })
        # Set secure cookies for tokens
        response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=60 * 60  # 1 hour
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=24 * 60 * 60  # 1 day
        )
        print(response)
        return response

#add service center view
class AddNewServiceCenterView(generics.CreateAPIView):
    queryset = ServiceCenter.objects.all()
    serializer_class = AddNewServiceCenter
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

# #view function to fetch all the service centers
# class ServiceCenterListView(generics.ListAPIView):
#     queryset = ServiceCenter.objects.all()  #get all service centers
#     serializer_class = ServiceCenterSerializer 
#     permission_classes = [permissions.AllowAny]


#user profile view
class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"detail": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT) 

class ServiceCenterViewSet(viewsets.ModelViewSet):
    queryset = ServiceCenter.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ServiceCenterUpdateSerializer
        return ServiceCenterSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsServiceCenterManager()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
#view class to get all the vehicles this is for customer
class GetAllVehiclesAPIView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = GetAllVehicleSerializer
    permission_classes = [permissions.AllowAny]

#add new vehicle
class AddNewVehicleView(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = AddNewVehicleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        # Ensure the user is a service manager
        if user.role != 'service_manager':
            raise PermissionDenied("Only service managers can add vehicles.")

        try:
            service_center = ServiceCenter.objects.get(center_manager=user)
        except ServiceCenter.DoesNotExist:
            raise PermissionDenied("You are not assigned to any service center.")

        # Save the vehicle and assign the service center
        serializer.save(sold_by=service_center)

class RetrieveUpdateDestroyVehicleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsServiceManagerAndOwner()]
    
#get all services for customers
class GetAllServicesAPIView(generics.ListAPIView):
    queryset = Servicing.objects.all()
    serializer_class = GetAllServicesSerializer
    permission_classes = [permissions.AllowAny]

#add new servce view
class AddNewServiceView(generics.CreateAPIView):
    def post(self, request):
        serializer = AddNewServiceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveUpdateDestroyServicesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicing.objects.all()
    serializer_class = ServiceDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsServiceManagerAndOwnerForServices()]