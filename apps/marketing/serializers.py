from rest_framework import serializers
from .models import MarketingMetrics, MarketingComponent
from apps.utils.baseSerializers import BaseCombinedSerializer

class MarketingComponentSerializer(BaseCombinedSerializer):
    class Meta:
        model = MarketingComponent
        fields = BaseCombinedSerializer.Meta.fields + ['type', 'cost']

class MarketingMetricsSerializer(BaseCombinedSerializer):
    components = MarketingComponentSerializer(many=True)

    class Meta:
        model = MarketingMetrics
        fields = BaseCombinedSerializer.Meta.fields + [
            'fiscal_year', 'yearly_marketing_cost', 'number_of_months_in_year', 
            'monthly_marketing_cost', 'cac', 'number_of_customers', 'components'
        ]
        read_only_fields = ['monthly_marketing_cost', 'number_of_customers']

    