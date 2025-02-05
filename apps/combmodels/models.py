from django.db import models
import uuid
from apps.accounts.models import CustomUser
from apps.financials.models import BaseModel


# MARKETING
class MarketingType(BaseModel):
    name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.cost}"


class Marketing(BaseModel):
    monthly_market_cost = models.ManyToManyField(MarketingType)
    yearly_market_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cust_acq_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subscript_count = models.PositiveIntegerField(default=0)
    subscript_dist = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    growth_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Marketing"
        verbose_name_plural = "Marketing"


class Customer(BaseModel):
    # Retention metrics
    ret_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    churn_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # Engagement metrics
    active_users = models.PositiveIntegerField(default=0)
    nps_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # Acquisition metrics
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    lead_qual_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Revenue(BaseModel):
    growth_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    avg_sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Growth and pricing
    growth_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    avg_sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #Volume and seasonality
    units_sold = models.PositiveIntegerField(default=0)
    seas_factor = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Revenue"
        verbose_name_plural = "Revenues"


class Operation(BaseModel):
    # Cost drivers
    materials_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overhead_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Departmental costs
    sales_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    marketing_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rd_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admin_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Employee metrics
    employee_count = models.PositiveIntegerField(default=0)
    avg_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sal_growth_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Operation"
        verbose_name_plural = "Operations"
