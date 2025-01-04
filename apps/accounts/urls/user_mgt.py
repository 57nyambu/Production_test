from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.accounts.views import (
    UpdateUserView,
    TestProtectedView,
    AdminUserViewSet,
    WelcomeView
)

router = DefaultRouter()
router.register('users', AdminUserViewSet, basename='user')

urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),
    path('profile/', UpdateUserView.as_view(), name='update-profile'),
    path('protected/', TestProtectedView.as_view(), name='protected'),
    path('user-details/', AdminUserViewSet.as_view({'get': 'list'}), name='user-details'),
] + router.urls
