import uuid
from django.db import models
from apps.accounts.models import CustomUser

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="%(class)ss")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomerModel(BaseModel):
    beginning_client = models.PositiveIntegerField(default=0)
    # Acquisition metrics
    conversion_rate = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    organic_client = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Customer Type: {self.cust_type},"
    
    
class CustomerDistribution(BaseModel):
    cust_model = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, related_name="distributions", null=True, blank=True)
    customer_type = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.customer_type} - {self.percentage}%"
    
    @staticmethod
    def calculate_distribution(user, total_customers):
        #Calculate customer distribution for a given user and total customers.
        distributions = CustomerDistribution.objects.filter(user=user)
        return [
            {
                "customer_type": dist.customer_type,
                "count": int(total_customers * float(dist.percentage) / 100),
                "percentage": float(dist.percentage),
            }
            for dist in distributions
        ]
    

class ChurnRate(BaseModel):
    cust_model = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, related_name="churn_rates", null=True, blank=True)
    year = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=5, decimal_places=2)