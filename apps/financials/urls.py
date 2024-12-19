from django.urls import path
from .views import CombinedCreateAPIView

urlpatterns = [
    # RevenueExpenses URLs
    path('models-create/', CombinedCreateAPIView.as_view(), name='models-create'),
]
