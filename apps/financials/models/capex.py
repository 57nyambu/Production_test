from django.db import models
from .company import CompanyInformation

class CapitalExpenditure(models.Model):
    company = models.OneToOneField(CompanyInformation, on_delete=models.CASCADE)
    total_ppe_value = models.DecimalField(max_digits=15, decimal_places=2)
    maintenance_capex = models.DecimalField(max_digits=15, decimal_places=2)
    growth_capex = models.DecimalField(max_digits=15, decimal_places=2)
    asset_lifespan = models.PositiveIntegerField()  # In years
    capitalized_costs = models.DecimalField(max_digits=15, decimal_places=2)
