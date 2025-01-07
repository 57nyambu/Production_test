from django.db import models
from apps.accounts.models import CustomUser
from django.utils import timezone

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=dict)
    period = models.PositiveIntegerField(null=True, blank=True)  # Made nullable
    
    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # Made nullable
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, null=True, blank=True)  # Made nullable
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.email if self.user else 'No User'} - {self.plan.name if self.plan else 'No Plan'}"