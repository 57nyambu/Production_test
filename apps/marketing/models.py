from django.db import models
import uuid
from apps.accounts.models import CustomUser

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
    yearly_marketing_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    number_of_months_in_year = models.IntegerField(default=12)
    
    cac = models.DecimalField(max_digits=15, decimal_places=2)  # Customer Acquisition Cost
    new_monthly_customers = models.PositiveIntegerField()
    growth_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Annual marketing cost {self.yearly_marketing_cost}"

class MarketingComponent(BaseModel):
    type = models.CharField(max_length=255)  # Example: "Social Media Ads", "Google Ads"
    cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.type} - ${self.cost}"
