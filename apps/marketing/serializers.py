from rest_framework import serializers
from .models import MarketingMetrics, MarketingComponent, GrowthRate
from apps.utils.baseSerializers import BaseCombinedSerializer


class MarketingComponentSerializer(BaseCombinedSerializer):
    class Meta:
        model = MarketingComponent
        fields = BaseCombinedSerializer.Meta.fields + ['type', 'cost']


class GrowthRateSerializer(BaseCombinedSerializer):
    class Meta:
        model = GrowthRate
        fields = BaseCombinedSerializer.Meta.fields + ['year', 'rate']


class MarketingMetricsSerializer(BaseCombinedSerializer):
    marketing_components = MarketingComponentSerializer(many=True, required=False)
    growth_rate = GrowthRateSerializer(many=True, required=False)

    class Meta:
        model = MarketingMetrics
        fields = BaseCombinedSerializer.Meta.fields + [
            'marketing_components', 'monthly_marketing_cost', 'yearly_marketing_cost',
            'cac', 'new_monthly_customers', 'growth_rate'
        ]


class GrowthProjectionSerializer(serializers.Serializer):
    """Serializer for growth projection output."""
    year = serializers.IntegerField()
    customers = serializers.IntegerField()


class CustomerTypeDistributionSerializer(serializers.Serializer):
    """Serializer for customer type distribution output."""
    customer_type = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)