from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('api/auth/', include('apps.accounts.urls.auth')),
    path('api/user-mgt/', include('apps.accounts.urls.user_mgt')),
    path('financials/', include('apps.financials.urls')),
    path('models/', include('apps.combmodels.urls')),
]
