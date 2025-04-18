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
    cust_distribution = CustomerDistributionSerializer(many=True, required=False)
    churn_rate = ChurnRateSerializer(many=True, required=False)
    class Meta(BaseCombinedSerializer.Meta):
        model = CustomerModel
        fields = BaseCombinedSerializer.Meta.fields + [
            "churn_rate", "cust_distribution", "beginning_client", "conversion_rate", "organic_client"
        ]        


class OrganicCustomerGrowthProjectionSerializer(serializers.Serializer):
    """Serializer for online customer growth projection."""
    year = serializers.IntegerField()
    customers = serializers.IntegerField()


class OrganicCustomerChurnRateSerializer(serializers.Serializer):
    """Serializer for online customer churn rate."""
    year = serializers.IntegerField()
    rate = serializers.DecimalField(max_digits=5, decimal_places=2)


class OrganicCustDistributionSerializer(serializers.Serializer):
    customer_type = serializers.CharField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)