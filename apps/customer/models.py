import uuid
from django.db import models
from django.contrib.auth import get_user_model
CustomUser = get_user_model()
from apps.marketing.models import MarketingMetrics


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="%(class)ss")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomerModel(BaseModel):
    churn_rate = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    customer_type = models.CharField(default='Organic', max_length=255)
    beginning_client = models.PositiveIntegerField(default=0)
    conversion_rate = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    organic_client = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Customer Type: {self.customer_type}"

    
