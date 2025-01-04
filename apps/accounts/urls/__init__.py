from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.accounts.urls.auth')),
    path('', include('apps.accounts.urls.user_mgt')),
]