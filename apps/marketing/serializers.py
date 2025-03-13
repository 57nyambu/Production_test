from rest_framework import serializers
from .models import MarketingMetrics, MarketingComponent
from apps.utils.baseSerializers import BaseCombinedSerializer

class MarketingComponentSerializer(BaseCombinedSerializer):
    class Meta:
        model = MarketingComponent
        fields = BaseCombinedSerializer.Meta.fields + ['type', 'cost']

class MarketingMetricsSerializer(BaseCombinedSerializer):
    marketing_components = MarketingComponentSerializer(many=True)

    class Meta:
        model = MarketingMetrics
        fields = BaseCombinedSerializer.Meta.fields + [
            'marketing_components',
            'fiscal_year', 'yearly_marketing_cost', 'number_of_months_in_year',
            'monthly_marketing_cost', 'cac', 'new_monthly_customers', 
        ]
        #read_only_fields = ['monthly_marketing_cost', 'cac']  # 'number_of_customers' removed since it's not in fields

    def validate(self, data):
        """
        Ensure that yearly_marketing_cost is non-negative and months are valid.
        """
        if data.get("yearly_marketing_cost", 0) < 0:
            raise serializers.ValidationError({"yearly_marketing_cost": "Marketing cost cannot be negative."})

        if data.get("number_of_months_in_year", 12) <= 0:
            raise serializers.ValidationError({"number_of_months_in_year": "Number of months must be greater than zero."})

        return data

    def create(self, validated_data):
        """
        Override to calculate derived fields before saving.
        """
        components_data = validated_data.pop("marketing_components", [])
        instance = MarketingMetrics.objects.create(**validated_data)

        # Create related components
        for component_data in components_data:
            MarketingComponent.objects.create(marketing_metrics=instance, **component_data)

        # Update calculated fields
        instance.monthly_marketing_cost = instance.yearly_marketing_cost / instance.number_of_months_in_year
        instance.cac = instance.yearly_marketing_cost / instance.new_monthly_customers if instance.new_monthly_customers > 0 else 0
        instance.save()

        return instance

    def update(self, instance, validated_data):
        """
        Update method to handle calculated fields and related components.
        """
        components_data = validated_data.pop("marketing_components", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Recalculate fields
        instance.monthly_marketing_cost = instance.yearly_marketing_cost / instance.number_of_months_in_year

        instance.save()

        # Update related components (this will remove old ones and create new ones)
        instance.marketing_components.all().delete()
        for component_data in components_data:
            MarketingComponent.objects.create(marketing_metrics=instance, **component_data)

        return instance
