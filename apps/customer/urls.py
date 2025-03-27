from django.urls import path
from .views import CustomerModelView, GrowthRateView

urlpatterns = [
    path("customer/", CustomerModelView.as_view(), name="customer-model"),
    path("growth-rate/", GrowthRateView.as_view(), name="growth-rate"),
]
