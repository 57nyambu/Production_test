from django.urls import path
from .views import MarketingCostView

urlpatterns = [
    path('marketing/', MarketingCostView.as_view(), name='Marketing Model')
]