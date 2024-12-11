from django.db import models
from .company import CompanyInformation

class FinancialModel(models.Model):
    company = models.OneToOneField(CompanyInformation, on_delete=models.CASCADE)
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    operating_expenses = models.DecimalField(max_digits=15, decimal_places=2)
    assets = models.DecimalField(max_digits=15, decimal_places=2)
    liabilities = models.DecimalField(max_digits=15, decimal_places=2)
    equity = models.DecimalField(max_digits=15, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.company.company_name} Financial Model"
