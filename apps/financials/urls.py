from django.urls import path
from .views import (
    RevenueExpensesCreateView, RevenueExpensesUpdateView,
    WorkingCapitalCreateView, WorkingCapitalUpdateView,
    IndustryMetricsCreateView, IndustryMetricsUpdateView,
    EmployeeSalaryInfoCreateView, EmployeeSalaryInfoUpdateView,
    CapitalExpenditureCreateView, CapitalExpenditureUpdateView
)

urlpatterns = [
    # RevenueExpenses URLs
    path('revenue-expenses/create/', RevenueExpensesCreateView.as_view(), name='revenue-expenses-create'),
    path('revenue-expenses/update/<int:pk>/', RevenueExpensesUpdateView.as_view(), name='revenue-expenses-update'),

    # WorkingCapital URLs
    path('working-capital/create/', WorkingCapitalCreateView.as_view(), name='working-capital-create'),
    path('working-capital/update/<int:pk>/', WorkingCapitalUpdateView.as_view(), name='working-capital-update'),

    # IndustryMetrics URLs
    path('industry-metrics/create/', IndustryMetricsCreateView.as_view(), name='industry-metrics-create'),
    path('industry-metrics/update/<int:pk>/', IndustryMetricsUpdateView.as_view(), name='industry-metrics-update'),

    # EmployeeSalaryInfo URLs
    path('employee-salary-info/create/', EmployeeSalaryInfoCreateView.as_view(), name='employee-salary-info-create'),
    path('employee-salary-info/update/<int:pk>/', EmployeeSalaryInfoUpdateView.as_view(), name='employee-salary-info-update'),

    # CapitalExpenditure URLs
    path('capital-expenditure/create/', CapitalExpenditureCreateView.as_view(), name='capital-expenditure-create'),
    path('capital-expenditure/update/<int:pk>/', CapitalExpenditureUpdateView.as_view(), name='capital-expenditure-update'),
]
