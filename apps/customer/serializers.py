from rest_framework import serializers
from .models import CustomerModel, CustomerDistribution, ChurnRate
from apps.marketing.models import GrowthRate
from apps.utils.baseSerializers import BaseCombinedSerializer

class GrowthRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthRate
        fields = ['year', 'rate']


class CustomerDistributionSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = CustomerDistribution
        fields = BaseCombinedSerializer.Meta.fields + ['customer_type', 'percentage']


class ChurnRateSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = ChurnRate
        fields = BaseCombinedSerializer.Meta.fields + ['year', 'rate']


class CustomerModelSerializer(BaseCombinedSerializer):
    cust_type = CustomerDistributionSerializer(many=True, required=False)
    churn_rate = ChurnRateSerializer(many=True, required=False)
    class Meta(BaseCombinedSerializer.Meta):
        model = CustomerModel
        fields = BaseCombinedSerializer.Meta.fields + [
            "churn_rate", "cust_type", "beginning_client", "conversion_rate", "organic_client"
        ]        


class OrganicCustomerYearMetricsSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    beginning_client = serializers.IntegerField()
    new_clients = serializers.IntegerField()
    churned_clients = serializers.IntegerField()
    closing_clients = serializers.IntegerField()


class OrganicCustomerMetricsSerializer(serializers.Serializer):
    organic_metrics = OrganicCustomerYearMetricsSerializer(many=True)


class OfflineCustomerYearMetricsSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    beginning_client = serializers.IntegerField()
    new_clients = serializers.IntegerField()
    churned_clients = serializers.IntegerField()
    closing_clients = serializers.IntegerField()


class PercentageDistributionSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    customer_type = serializers.CharField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    january_value = serializers.IntegerField()


class OfflineCustomerMetricsSerializer(serializers.Serializer):
    offline_metrics = OfflineCustomerYearMetricsSerializer(many=True)
    percentage_distributions = PercentageDistributionSerializer(many=True)


class CombinedCustomerMetricsSerializer(serializers.Serializer):
    organic = OrganicCustomerMetricsSerializer(allow_null=True)
    offline = OfflineCustomerMetricsSerializer(allow_null=True)