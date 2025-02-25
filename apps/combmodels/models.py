from django.db import models
from apps.financials.models import BaseModel

class MarketingCost(BaseModel):
    social_media_ads = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    google_ads = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    physical_marketing = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bill_boards = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_marketing = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    @property
    def yearly_marketing_cost(self):
        return (self.social_media_ads or 0 + self.google_ads or 0 + self.physical_marketing or 0 +
                self.bill_boards or 0 + self.other_marketing or 0) * 12

class CustomerAcquisition(BaseModel):
    marketing_cost = models.ForeignKey(MarketingCost, on_delete=models.CASCADE)
    customer_acquisition_cost = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_subscribers = models.IntegerField(null=True, blank=True)
    subscriber_1_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=70.0)
    subscriber_2_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=30.0)
    
    @property
    def calculated_subscribers(self):
        if self.customer_acquisition_cost > 0:
            return self.marketing_cost.yearly_marketing_cost / self.customer_acquisition_cost
        return 0

class GrowthRate(BaseModel):
    year = models.IntegerField()
    growth_rate = models.DecimalField(max_digits=5, decimal_places=2)

class ClientSegment(BaseModel):
    segment_name = models.CharField(max_length=255)
    number_of_clients = models.IntegerField()
    year = models.IntegerField()
    
class CustomerAcquisitionCost(BaseModel):
    social_media_ads = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    google_ads = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    average_cost_per_click = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    leads_generated = models.IntegerField(null=True, blank=True)
    percentage_conversion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    other_marketing_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offline_customers_acquired = models.IntegerField(null=True, blank=True)
    organic_customers_acquired = models.IntegerField(null=True, blank=True)
    
    @property
    def number_of_customers(self):
        if self.percentage_conversion and self.leads_generated:
            return int(self.leads_generated * (self.percentage_conversion / 100))
        return 0
    
    @property
    def total_marketing_cost(self):
        return (self.social_media_ads or 0) + (self.google_ads or 0) + (self.other_marketing_cost or 0)
    
    @property
    def cac(self):
        total_customers = self.number_of_customers + (self.offline_customers_acquired or 0)
        return self.total_marketing_cost / total_customers if total_customers > 0 else 0
