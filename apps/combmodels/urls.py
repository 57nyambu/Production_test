from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MarketingViewSet
)

router = DefaultRouter()
router.register('marketing', MarketingViewSet)

urlpatterns = [
    path('models/', include(router.urls)),
]