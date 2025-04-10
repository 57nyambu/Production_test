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
        fields = BaseCombinedSerializer.Meta.fields + ['year', 'churn_rate']


class CustomerModelSerializer(BaseCombinedSerializer):
    cust_distribution = CustomerDistributionSerializer(many=True, required=False)
    churn_rate = ChurnRateSerializer(many=True, required=False)
    class Meta(BaseCombinedSerializer.Meta):
        model = CustomerModel
        fields = BaseCombinedSerializer.Meta.fields + [
            "growth_rate", "churn_rate", "cust_distribution", "beginning_client", "conversion_rate", "organic_client"
        ]        


