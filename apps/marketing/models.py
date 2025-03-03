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
    fiscal_year = models.IntegerField(unique=True)  # Ensure unique fiscal year
    yearly_marketing_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    number_of_months_in_year = models.IntegerField(default=12)
    monthly_marketing_cost = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    cac = models.DecimalField(max_digits=15, decimal_places=2)  # Customer Acquisition Cost
    number_of_customers = models.IntegerField(editable=False)  # Auto-calculated field

    def save(self, *args, **kwargs):
        # Calculate yearly marketing cost based on related components
        total_cost = sum(self.marketing_components.values_list('cost', flat=True))
        self.yearly_marketing_cost = total_cost
        self.monthly_marketing_cost = self.yearly_marketing_cost / self.number_of_months_in_year

        # Avoid division by zero
        self.number_of_customers = (
            int(self.monthly_marketing_cost / self.cac) if self.cac > 0 else 0
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Marketing Metrics for FY{self.fiscal_year}"


class MarketingComponent(BaseModel):
    marketing_metrics = models.ForeignKey(MarketingMetrics, related_name="marketing_components", on_delete=models.CASCADE)
    type = models.CharField(max_length=255)  # Example: "Social Media Ads", "Google Ads"
    cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.type} - ${self.cost}"
