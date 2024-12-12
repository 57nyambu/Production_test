from django.urls import path
from .views import RegisterUserView, LoginView, LogoutView, TestProtectedView, WelcomeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),  # Root URL for the welcome page
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('protected/', TestProtectedView.as_view(), name='protected'),
]
