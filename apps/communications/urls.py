from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EmailsAPIView,
    RecievedEmailsAPIView
)

urlpatterns = [
    path('emails/', EmailsAPIView.as_view(), name='emails'),
    path('recievedemails/', RecievedEmailsAPIView.as_view(), name='recievedemails'),
]