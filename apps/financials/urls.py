from django.urls import path
from .views import CombinedCreateAPIView, CombinedUpdateAPIView

urlpatterns = [
    # RevenueExpenses URLs
    path('models-create/', CombinedCreateAPIView.as_view(), name='models-create'),
    path('models-update/', CombinedUpdateAPIView.as_view(), name='models-update'),
]
