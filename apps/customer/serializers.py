from rest_framework import serializers
from .models import CustomerModel
from apps.marketing.models import GrowthRate
from apps.financials.models import CompanyInformation
from apps.utils.baseSerializers import BaseCombinedSerializer

class GrowthRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthRate
        fields = ['year', 'rate']


class CompanyInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInformation
        fields = ['company_name', 'industry', 'company_stage']


class CustomerModelSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = CustomerModel
        fields = BaseCombinedSerializer.Meta.fields + [
            "churn_rate", "customer_type", "beginning_client", "conversion_rate", "organic_client"
        ]        


