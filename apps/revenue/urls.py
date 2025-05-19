from .views import RevenueView, RevenueOutputView
from apps.financials.views import RevenueDriversAPIView
from django.urls import path

urlpatterns = [
    path('revenue/', RevenueDriversAPIView.as_view(), name='revenue-model'),
    path('output/revenue/', RevenueOutputView.as_view(), name='revenue-output')
] 