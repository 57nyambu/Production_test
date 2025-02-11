from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyInformationViewSet,
    WorkingCapitalViewSet,
    RevenueDriversViewSet,
    CostStractureViewSet,
    AllExpensesViewSet,
    CapexViewSet,
    DividendPolicyViewSet,
    IndustryMetricsViewSet,
    HistoricalFinDataViewSet,
)

router = DefaultRouter()
router.register('company-info', CompanyInformationViewSet)
router.register('working-capital', WorkingCapitalViewSet)
router.register('revenue-drivers', RevenueDriversViewSet)
router.register('cost-stracture', CostStractureViewSet)
router.register('all-expenses', AllExpensesViewSet)
router.register('capital-exp', CapexViewSet)
router.register('dividend-policy', DividendPolicyViewSet)
router.register('industry-metrics', IndustryMetricsViewSet)
router.register('historical-fin-data', HistoricalFinDataViewSet)


urlpatterns = [
    path('models/', include(router.urls)),
]
