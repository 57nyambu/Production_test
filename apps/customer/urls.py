from django.urls import path
from .views import CustomerModelView, CombinedCustomerMetricsView

urlpatterns = [
    path("customer/", CustomerModelView.as_view(), name="customer-model"),
    path("output/customer/", CombinedCustomerMetricsView.as_view(), name="customer-output"),
]
