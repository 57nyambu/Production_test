import uuid
from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="%(class)ss")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomerModel(BaseModel):
    fiscal_year = models.IntegerField(choices=[(i, f"FY{i}") for i in range(1, 6)])

    # **User Inputs**
    beginning_monthly_clients = models.IntegerField()
    additional_new_clients_per_month = models.IntegerField()
    growth_rate = models.DecimalField(max_digits=5, decimal_places=2)
    churn_rate = models.DecimalField(max_digits=5, decimal_places=2)

    # **Auto-Calculated Fields**
    churned_clients_per_month = models.IntegerField(editable=False)
    closing_monthly_clients = models.IntegerField(editable=False)

    def save(self, *args, **kwargs):
        """Automatically calculate churned clients and closing clients before saving."""
        self.churned_clients_per_month = int(self.additional_new_clients_per_month * float(self.churn_rate))
        self.closing_monthly_clients = (
            self.beginning_monthly_clients + self.additional_new_clients_per_month - self.churned_clients_per_month
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"CustomerModel: FY{self.fiscal_year} | User: {self.user.username}"


class CustomerPercentageDistribution(BaseModel):
    fiscal_year = models.IntegerField(choices=[(i, f"FY{i}") for i in range(1, 6)])
    month = models.IntegerField(choices=[(i, i) for i in range(1, 13)])  # 1 to 12 months

    # **User Input**
    closing_customers = models.IntegerField()

    # **Auto-Calculated Fields**
    subscription_percentage = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    other_services_percentage = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        """Calculate percentages before saving."""
        subscription_ratio = 0.6  # Assume 60% go to subscriptions
        self.subscription_percentage = self.closing_customers * subscription_ratio
        self.other_services_percentage = self.closing_customers * (1 - subscription_ratio)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"CustomerPercentage: FY{self.fiscal_year} | Month {self.month}"
