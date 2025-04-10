from django.urls import path
from .views import CustomerModelView

urlpatterns = [
    path("customer/", CustomerModelView.as_view(), name="customer-model"),
]
