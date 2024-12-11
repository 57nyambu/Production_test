from django.db import models
from .company import CompanyInformation

class WorkingCapital(models.Model):
    company = models.OneToOneField(CompanyInformation, on_delete=models.CASCADE)
    days_receivables = models.DecimalField(max_digits=5, decimal_places=2)
    days_inventory = models.DecimalField(max_digits=5, decimal_places=2)
    days_payables = models.DecimalField(max_digits=5, decimal_places=2)
    working_capital_days = models.DecimalField(max_digits=5, decimal_places=2)
