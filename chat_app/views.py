from django.shortcuts import render
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, ChatMessage
from .serializers import MessageSerializer, ProfileSerializer

class GetMessagesListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        #fetch all unique users the current user has chatted with
        message_partners = User.objects.filter(
            Q(sender__receiver=user) | Q(receiver__sender=user)
        ).distinct()

        #collect chat messages between current user and each partner
        all_messages = ChatMessage.objects.filter(
            Q(sender=user, receiver__in=message_partners) |
            Q(sender__in=message_partners, receiver=user)
        ).order_by('date')

        return all_messages

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SendMessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


class ReadMessagesUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sender_id = self.request.user.id
        receiver_id = self.kwargs['receiver_id']

        return ChatMessage.objects.filter(
            Q(sender=sender_id, receiver=receiver_id) | Q(sender=receiver_id, receiver=sender_id),
            is_read=False
        )

    def update(self, request, *args, **kwargs):
        updated_count = self.get_queryset().update(is_read=True)
        if updated_count:
            return Response({'message': 'Messages marked as read'})
        return Response({'message': 'No unread messages found'})


class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        return User.objects.filter(
            Q(username__icontains=username) |
            Q(first_name__icontains=username) |
            Q(last_name__icontains=username) |
            Q(email__icontains=username)
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'detail': 'Users not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
