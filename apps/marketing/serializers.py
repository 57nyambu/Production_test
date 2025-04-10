from rest_framework import serializers
from .models import MarketingMetrics, MarketingComponent, GrowthRate
from apps.utils.baseSerializers import BaseCombinedSerializer
from apps.customer.models import CustomerDistribution

cust_type = CustomerDistribution.objects.values_list('customer_type', flat=True).distinct()

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


# Serializers
class GrowthProjectionSerializer(serializers.Serializer):
    """Serializer for growth projection input parameters."""
    initial_customers = serializers.IntegerField(min_value=1)
    growth_rates = serializers.ListField(
        child=serializers.FloatField(min_value=0),
        help_text="List of growth rates as percentages (e.g., 5.0 for 5%)"
    )
    
    def validate(self, data):
        """Validate that at least one growth rate is provided."""
        if not data.get('growth_rates'):
            raise serializers.ValidationError("At least one growth rate must be provided")
        return data
    
    
class GrowthProjectionSerializer(serializers.Serializer):
    """Serializer for growth projection output."""
    year = serializers.IntegerField()
    customers = serializers.IntegerField()


class CustomerTypeDistributionSerializer(serializers.Serializer):
    """Serializer for customer type distribution output."""
    customer_type = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)