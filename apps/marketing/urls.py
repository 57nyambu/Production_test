from django.urls import path
from .views import MarketingMetricsView

urlpatterns = [
    path('marketing/', MarketingMetricsView.as_view(), name='Marketing Model')
]