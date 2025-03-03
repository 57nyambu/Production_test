from rest_framework import serializers
from .models import CustomerModel, CustomerPercentageDistribution
from apps.utils.baseSerializers import BaseCombinedSerializer

class CustomerModelSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = CustomerModel
        fields = BaseCombinedSerializer.Meta.fields + [
            "fiscal_year", "beginning_monthly_clients", "additional_new_clients_per_month", 
            "growth_rate", "churn_rate", "churned_clients_per_month", "closing_monthly_clients"
        ]
        read_only_fields = BaseCombinedSerializer.Meta.fields + ["churned_clients_per_month", "closing_monthly_clients"]


class CustomerPercentageDistributionSerializer(serializers.ModelSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = CustomerPercentageDistribution
        fields = BaseCombinedSerializer.Meta.fields + [
            "fiscal_year", "month", "closing_customers",
            "subscription_percentage", "other_services_percentage"
        ]
        read_only_fields = BaseCombinedSerializer.Meta.fields + ["subscription_percentage", "other_services_percentage"]
