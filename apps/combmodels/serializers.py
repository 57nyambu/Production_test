from rest_framework import serializers
from django.db import transaction
from apps.utils.baseSerializers import BaseModelSerializer, BaseCombinedSerializer
from .models import (
    MarketingCost,
    CustomerAcquisition,
    GrowthRate,
    ClientSegment,
    CustomerAcquisitionCost
)

class MarketingCostSerializer(BaseModelSerializer):
    class Meta:
        model = MarketingCost
        fields = ['social_media_ads', 'google_ads', 'physical_marketing', 'bill_boards', 'other_marketing', 'yearly_marketing_cost']

class CustomerAcquisitionSerializer(BaseModelSerializer):
    marketing_cost = MarketingCostSerializer(read_only=True)
    
    class Meta:
        model = CustomerAcquisition
        fields = ['marketing_cost', 'customer_acquisition_cost', 'number_of_subscribers', 'subscriber_1_percentage', 'subscriber_2_percentage', 'calculated_subscribers']

class GrowthRateSerializer(BaseModelSerializer):
    class Meta:
        model = GrowthRate
        fields = ['year', 'growth_rate']

class ClientSegmentSerializer(BaseModelSerializer):
    class Meta:
        model = ClientSegment
        fields = ['segment_name', 'number_of_clients', 'year']

class CustomerAcquisitionCostSerializer(BaseModelSerializer):
    class Meta:
        model = CustomerAcquisitionCost
        fields = ['social_media_ads', 'google_ads', 'average_cost_per_click', 'leads_generated', 'percentage_conversion', 'other_marketing_cost', 'offline_customers_acquired', 'organic_customers_acquired', 'number_of_customers', 'total_marketing_cost', 'cac']

class CombinedMarketSerializer(BaseCombinedSerializer):
    marketing_cost = MarketingCostSerializer(required=False)
    customer_acquisition = CustomerAcquisitionSerializer(required=False)
    growth_rate = GrowthRateSerializer(required=False)
    client_segment = ClientSegmentSerializer(required=False)
    customer_acquisition_cost = CustomerAcquisitionCostSerializer(required=False)
    