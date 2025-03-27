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


class RevenueModel(BaseModel):
    percentage_comm = models.DecimalField(default=0 ,max_digits=5, decimal_places=2)
    units_sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Percentage Commission: {self.percentage_comm}, Units Sold: {self.units_sold}"

