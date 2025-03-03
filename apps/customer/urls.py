from django.urls import path
from .views import CustomerModelView, CustomerPercentageDistributionView

urlpatterns = [
    path("customer-model/", CustomerModelView.as_view(), name="customer-model"),
    path("customer-percentage-distribution/", CustomerPercentageDistributionView.as_view(), name="customer-percentage-distribution"),
]
