from django.urls import path
from .views import CustomerModelView, CombinedCustomerMetricsView, RevenueDriversView

urlpatterns = [
    path("customer/", CustomerModelView.as_view(), name="customer-model"),
    path("output/customer/", CombinedCustomerMetricsView.as_view(), name="customer-output"),
    path("revenue-stream/", RevenueDriversView.as_view(), name="revenue-stream-model"),
]
