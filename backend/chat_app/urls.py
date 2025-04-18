from django.urls import path
from .views import *

urlpatterns = [
    path("get-messages/", GetMessagesListAPIView.as_view()),
    path('send/', SendMessageCreateAPIView.as_view(), name='send-message'),
    path('read/<int:receiver_id>/', ReadMessagesUpdateAPIView.as_view(), name='read-messages'),
    path('search/', SearchUserAPIView.as_view(), name='search_user'),
]
