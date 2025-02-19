from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MarketingAPIView
)

urlpatterns = [
    path('marketing/', MarketingAPIView.as_view(), name='marketing'),
]