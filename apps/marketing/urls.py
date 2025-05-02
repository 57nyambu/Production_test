from django.urls import path
from .views import MarketingMetricsView, GrowthProjectionView

urlpatterns = [
    path('marketing/', MarketingMetricsView.as_view(), name='Marketing Model'),
    path('output/marketing/', GrowthProjectionView.as_view(), name='Marketing Model Read Only'),
]