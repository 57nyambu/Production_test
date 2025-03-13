from rest_framework import serializers
from .models import MarketingMetrics, MarketingComponent
from apps.utils.baseSerializers import BaseCombinedSerializer

class MarketingComponentSerializer(BaseCombinedSerializer):
    class Meta:
        model = MarketingComponent
        fields = BaseCombinedSerializer.Meta.fields + ['type', 'cost']

class MarketingMetricsSerializer(BaseCombinedSerializer):
    marketing_components = MarketingComponentSerializer(many=True, required=False)

    class Meta:
        model = MarketingMetrics
        fields = BaseCombinedSerializer.Meta.fields + [
            'marketing_components', 'monthly_marketing_cost', 'yearly_marketing_cost',
            'cac', 'new_monthly_customers', 'growth_rate'
        ]

    