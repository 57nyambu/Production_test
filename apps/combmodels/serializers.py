from rest_framework import serializers
from django.db import models
from apps.financials.serializers.core import BaseModelSerializer, NestedManyToManyMixin
from .models import (MarketingType,
                    Marketing, 
                     Customer, 
                     Revenue, 
                     Operation)

class MarketingTypeSerializer(BaseModelSerializer):
    class Meta:
        model = MarketingType
        fields = fields = BaseModelSerializer.Meta.fields +[
            'name', 'cost']


class MarketingSerializer(BaseModelSerializer, NestedManyToManyMixin):
    market_type = MarketingTypeSerializer(many=True, required=False)
    class Meta:
        model = Marketing
        fields = fields = BaseModelSerializer.Meta.fields +[
            'market_type', 'monthly_market_cost', 'yearly_market_cost', 'cust_acq_cost',
              'subscript_count', 'subscript_dist', 'growth_rate']
        
