from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EmailsAPIView,
    EmailsListAPIView
)

urlpatterns = [
    path('emails/', EmailsAPIView.as_view(), name='emails'),
    path('available-emails/', EmailsListAPIView.as_view(), name='Available-emails'),
]