from .views import RevenueView, RevenueOutputView
from django.urls import path

urlpatterns = [
    path('revenue/', RevenueView.as_view(), name='revenue-model'),
    path('output/revenue/', RevenueOutputView.as_view(), name='revenue-output')
] 