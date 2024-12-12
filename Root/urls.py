from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('apps.accounts.urls')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
]
