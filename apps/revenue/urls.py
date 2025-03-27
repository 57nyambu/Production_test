from .views import RevenueView
from django.urls import path

urlpatterns = [
    path('revenue/', RevenueView.as_view(), name='revenue-model'),
] 