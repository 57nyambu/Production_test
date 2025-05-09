from django.urls import path

from .views import IncomeOutputView

urlpatterns = [
    path('output/income-statement/', IncomeOutputView.as_view(), name="income-statement")
]