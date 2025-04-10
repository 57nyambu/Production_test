from .views import RevenueView, RevenueStreamView
from django.urls import path

urlpatterns = [
    path('revenue/', RevenueView.as_view(), name='revenue-model'),
    path('output/revenue/', RevenueStreamView.as_view(), name='revenue-output'),
] 