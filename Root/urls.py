from django.contrib import admin
from django.urls import path, include
from django.contrib.admin.views.decorators import staff_member_required
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("api/schema/", staff_member_required(SpectacularAPIView.as_view()), name="schema"),
    path("api/docs/swagger/", staff_member_required(SpectacularSwaggerView.as_view(url_name="schema")), name="swagger-ui"),
    path("api/docs/redoc/", staff_member_required(SpectacularRedocView.as_view(url_name="schema")), name="redoc"),
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
