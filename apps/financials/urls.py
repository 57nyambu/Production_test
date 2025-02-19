from django.urls import path
#from rest_framework.documentation import include_docs_urls
from .views import (
    CompanyInformationAPIView,
    WorkingCapitalAPIView,
    RevenueDriversAPIView,
    CostStractureAPIView,
    AllExpensesAPIView,
    CapexAPIView,
    DividendPolicyAPIView,
    IndustryMetricsAPIView,
    HistoricalFinDataAPIView,
)


urlpatterns = [
    path('company-info/', CompanyInformationAPIView.as_view(), name='company_info'),
    path('working-capital/', WorkingCapitalAPIView.as_view(), name='working_capital'),
    path('revenue-drivers/', RevenueDriversAPIView.as_view(), name='revenue_drivers'),
    path('cost-stracture/', CostStractureAPIView.as_view(), name='cost_stracture'),
    path('all-expenses/', AllExpensesAPIView.as_view(), name='all_expenses'),
    path('capex/', CapexAPIView.as_view(), name='capex'),
    path('dividend-policy/', DividendPolicyAPIView.as_view(), name='dividend_policy'),
    path('industry-metrics/', IndustryMetricsAPIView.as_view(), name='industry_metrics'),
    path('historical-fin-data/', HistoricalFinDataAPIView.as_view(), name='historical_fin_data'),
]