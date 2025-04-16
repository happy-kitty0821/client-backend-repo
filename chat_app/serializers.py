from rest_framework import serializers
from django.conf import settings
from .models import User, ChatMessage

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture', 'phone_number', 'role']

class MessageSerializer(serializers.ModelSerializer):
    sender_profile = ProfileSerializer(source='sender', read_only=True)
    receiver_profile = ProfileSerializer(source='receiver', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'message', 'date', 'is_read', 'sender_profile', 'receiver_profile']
