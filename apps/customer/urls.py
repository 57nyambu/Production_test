from django.urls import path
from .views import CustomerModelView, OrganicCustomerMetricsView

urlpatterns = [
    path("customer/", CustomerModelView.as_view(), name="customer-model"),
    path("output/customer/", OrganicCustomerMetricsView.as_view(), name="customer-output"),
]
