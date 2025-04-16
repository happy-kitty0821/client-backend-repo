from rest_framework import serializers
from .models import *

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role', 'phone_number', 'address', 'city', 'country', 'profile_picture']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # remove it as we don’t store it
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # hash the password
        user.save()
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

#class to add new service center
class AddNewServiceCenter(serializers.ModelSerializer):
    class Meta:
        model = ServiceCenter
        fields = ['name', 'description', 'location', 'open_time', 'close_time', 'center_manager', 'center_logo']

    def validate_center_manager(self, value):
        # Check if the user exists
        try:
            user = User.objects.get(id=value.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        # Validate that the user has the 'service_manager' role
        if user.role != 'service_manager':
            raise serializers.ValidationError("The user must be registered as a Manager")

        return value

#a serializer for the User model (for center_manager)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']  # include only the username field

#rhe ServiceCenter serializer to use the UserSerializer
class ServiceCenterSerializer(serializers.ModelSerializer):
    center_manager = UserSerializer(read_only=True)  # Nested read-only

    class Meta:
        model = ServiceCenter
        fields = ['center_id', 'name', 'description', 'location', 'open_time', 'close_time', 'center_manager', 'center_logo']


class ServiceCenterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCenter
        fields = ['name', 'description', 'location', 'open_time', 'close_time', 'center_manager', 'center_logo']

    def validate_center_manager(self, value):
        try:
            user = User.objects.get(id=value.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        if user.role != 'service_manager':
            raise serializers.ValidationError("The user must be a service manager.")
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','role','phone_number','address','city','country','profile_picture']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'role': {'read_only': True}  #stop thje users from changing their role
        }


class GetAllVehicleSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='sold_by.name', read_only=True) # Nested read-only
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'make', 'model', 'year', 'description', 'vin', 'image', 'price', 'discount', 'sold_by', 'center_name']  

#class to add new vehicle
class AddNewVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'description', 'vin', 'image', 'price', 'discount']

    def validate_center_manager(self, value):
        # Check if the user exists
        try:
            user = User.objects.get(id=value.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        # Validate that the user has the 'service_manager' role
        if user.role != 'service_manager':
            raise serializers.ValidationError("The user must be registered as a Manager")

        return value

class VehicleDetailSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='sold_by.name', read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'vehicle_id', 'make', 'model', 'year', 'description',
            'vin', 'image', 'price', 'discount', 'sold_by', 'center_name'
        ]
        read_only_fields = ['sold_by']


#services
class GetAllServicesSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='provided_by.name', read_only=True)  # Nested read-only field

    class Meta:
        model = Servicing
        fields = ['service_id', 'name', 'description', 'image', 'cost', 'discount', 'center_name', 'provided_by']

#class to add a new service
class AddNewServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicing
        fields = ['name', 'description', 'cost', 'image', 'discount']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        # Check if the user is a valid service_manager
        if not user or user.role != 'service_manager':
            raise serializers.ValidationError("Only a service manager can create a service.")

        # Get the related service center
        try:
            service_center = ServiceCenter.objects.get(center_manager=user)
        except ServiceCenter.DoesNotExist:
            raise serializers.ValidationError("This manager is not assigned to any service center.")

        # Attach the foreign key (provided_by) before saving
        return Servicing.objects.create(provided_by=service_center, **validated_data)
    
class ServiceDetailSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='provided_by.name', read_only=True)

    class Meta:
        model = Servicing
        fields = [
            'service_id', 'name', 'description', 'image', 'cost', 'discount', 'provided_by', 'center_name'
        ]
        read_only_fields = ['provided_by']