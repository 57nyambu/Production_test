from django.db import models
import uuid
from apps.accounts.models import CustomUser
from apps.customer.models import CustomerModel


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="%(class)ss")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MarketingMetrics(BaseModel):
    marketing_components = models.ManyToManyField('MarketingComponent')
    monthly_marketing_cost = models.DecimalField(max_digits=15, decimal_places=2)
    yearly_marketing_cost = models.DecimalField(max_digits=15, decimal_places=2)
    cac = models.DecimalField(max_digits=15, decimal_places=2, null=True)  # Customer Acquisition Cost
    new_monthly_customers = models.PositiveIntegerField()
    growth_rate = models.ManyToManyField('GrowthRate')

    def __str__(self):
        return f"yearly cost:{self.yearly_marketing_cost}"
    
    def calculate_growth_projections(self, begining_customer=None):
        """Calculate yearly growth projections."""
        total_customers = self.new_monthly_customers + begining_customer
        projections = []
        growth_rates = self.growth_rate.all().order_by('year')
        for growth in growth_rates:
            projections.append({
                "year": growth.year,
                "customers": int(total_customers)
            })
            total_customers *= (1 + float(growth.rate) / 100)
        return projections

class MarketingComponent(BaseModel):
    market_metrics = models.ForeignKey(MarketingMetrics, on_delete=models.CASCADE, related_name='components', null=True, blank=True)
    type = models.CharField(max_length=255)  # Example: "Social Media Ads", "Google Ads"
    cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.type} - ${self.cost}"


class GrowthRate(BaseModel):
    marketing_metrics = models.ForeignKey(MarketingMetrics, on_delete=models.CASCADE, related_name='growth_rates', null=True, blank=True)
    year = models.IntegerField()
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.year} - {self.rate}"