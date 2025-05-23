from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('api/auth/', include('apps.accounts.urls.auth')),
    path('api/user-mgt/', include('apps.accounts.urls.user_mgt')),
    path('financials/', include('apps.financials.urls')),
    path('models/', include('apps.marketing.urls')),
    path('models/', include('apps.customer.urls')),
    path('models/', include('apps.revenue.urls')),
    path('statements/', include('apps.statements.urls')),
    path('communications/', include('apps.communications.urls')),
]
