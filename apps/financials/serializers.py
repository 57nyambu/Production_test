from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from typing import Dict, Any, Type, List, Optional
from django.db.models import Model
from .models import (
    CompanyInformation, WorkingCapital, RevenueStream, RevenueDrivers,
    CostStracture, EmployeeInfo, AdminMarketingExp, AllExpenses,
    Asset, Capex, DividendPolicy, IndustryMetrics,HistoricalFinData, 
)
# Don't even think about touching it, validating req fields
class RequiredFieldsMixin:
    required_fields = []

    def validate(self, data):
        missing_fields = [
            field for field in self.required_fields 
            if field not in data or data[field] is None
        ]
        if missing_fields:
            raise serializers.ValidationError({field: f"{field} is required." for field in missing_fields})
        return data


# Serializers
class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CompanyInformationSerializer(BaseModelSerializer):
    fiscal_year_end = serializers.DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])
    class Meta(BaseModelSerializer.Meta):
        model = CompanyInformation
        fields = BaseModelSerializer.Meta.fields + [
            'company_name', 'industry', 'company_stage', 'funding_type', 'fiscal_year_end'
        ]


class WorkingCapitalSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = WorkingCapital
        fields = BaseModelSerializer.Meta.fields + [
            'days_receivables', 'days_inventory', 'days_payables', 'working_capital_days'
        ]


class RevenueStreamSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = RevenueStream
        fields = BaseModelSerializer.Meta.fields + [
            'name', 'type', 'amount'
        ]


class RevenueDriversSerializer(RequiredFieldsMixin, BaseModelSerializer):
    required_fields = ['average_selling_price', 'units_sold',]
    revenue_streams = RevenueStreamSerializer(many=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = RevenueDrivers
        fields = BaseModelSerializer.Meta.fields + [
            'average_selling_price', 'units_sold', 'revenue_streams'
        ]


class CostStractureSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = CostStracture
        fields = BaseModelSerializer.Meta.fields + [
            'raw_material', 'direct_labor', 'man_overhead', 'total_cogs',
            'fixed_cost', 'variable_cost', 'cd_raw_material', 'cd_direct_labor', 'cd_man_overhead'
        ]


class EmployeeInfoSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = EmployeeInfo
        fields = BaseModelSerializer.Meta.fields + [
            'position', 'salary', 'count', 'salary_growth_rate'
        ]


class AdminMarketingExpSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = AdminMarketingExp
        fields = BaseModelSerializer.Meta.fields + [
            'exp_type', 'amount', 'description'
        ]


class AllExpensesSerializer(RequiredFieldsMixin ,BaseModelSerializer):
    required_fields = ['average_selling_price', 'units_sold']
    employee_info = EmployeeInfoSerializer(many=True, required=False)
    admin_marketing_exp = AdminMarketingExpSerializer(many=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = AllExpenses
        fields = BaseModelSerializer.Meta.fields + [
            'employee_info', 'average_selling_price', 'units_sold', 'admin_marketing_exp'
        ]

class AssetSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Asset
        fields = BaseModelSerializer.Meta.fields + [
            'name', 'value', 'type', 'description'
        ]


class CapexSerializer(RequiredFieldsMixin, BaseModelSerializer):
    required_fields = ['maintenance_capex', 'growth_capex', 'asset_lifespan', 'capitalized_costs']
    assets = AssetSerializer(many=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = Capex
        fields = BaseModelSerializer.Meta.fields + [
            'maintenance_capex', 'growth_capex', 'asset_lifespan', 'capitalized_costs', 'assets'
        ]


class DividendPolicySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = DividendPolicy
        fields = BaseModelSerializer.Meta.fields + [
            'payout_ratio', 'div_per_share', 'div_growth_rt'
        ]


class IndustryMetricsSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = IndustryMetrics
        fields = BaseModelSerializer.Meta.fields + [
            'market_share', 'industry_growth_rate', 'competitor_count', 'market_size',
            'corporate_tax_rate', 'inflation_rate', 'gdp_growth_rate', 'interest_rate'
        ]


class HistoricalFinDataSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = HistoricalFinData
        fields = BaseModelSerializer.Meta.fields + [
            'revenue', 'cogs', 'salaries', 'rent', 'marketing', 'technology', 
            'insurance', 'other', 'total_operating_expenses', 'cash_equivs', 
            'acc_receivable', 'inventory', 'fixed_assets', 'acc_payable', 
            'short_debt', 'long_debt', 'paid_in_cap', 'retained_earning'
        ]

#combined serializer 


class CombinedSerializer(serializers.Serializer):
    company_information = CompanyInformationSerializer(required=False)
    working_capital = WorkingCapitalSerializer(required=False)
    revenue_drivers = RevenueDriversSerializer(required=False)
    cost_structure = CostStractureSerializer(required=False)
    all_expenses = AllExpensesSerializer(required=False)
    capex = CapexSerializer(required=False)
    dividend_policy = DividendPolicySerializer(required=False)
    industry_metrics = IndustryMetricsSerializer(required=False)
    historical_fin_data = HistoricalFinDataSerializer(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pass request context to child serializers
        context = kwargs.get('context', {})
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.BaseSerializer):
                field.context.update(context)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, field in self.fields.items():
            if field_name in representation and isinstance(field, serializers.BaseSerializer):
                field.context.update(self.context)
        return representation

    def to_internal_value(self, data):
        user = self.context['request'].user
        for key, value in data.items():
            if isinstance(value, dict):
                value['user'] = user.id
                for nested_key, nested_value in value.items():
                    if isinstance(nested_value, list):
                        for item in nested_value:
                            if isinstance(item, dict):
                                item['user'] = user.id
                    elif isinstance(nested_value, dict):
                        nested_value['user'] = user.id
        return super().to_internal_value(data)

    def _get_model_and_serializer(self, key: str) -> tuple[Type[Model], serializers.Serializer]:
        serializer = self.fields[key]
        if hasattr(serializer, 'child'):
            model_class = serializer.child.Meta.model
        else:
            model_class = serializer.Meta.model
        return model_class, serializer

    def _handle_nested_data(self, data: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, List[Model]]]:
        nested_data = {}
        nested_instances = {}
        for field_name, value in data.items():
            if isinstance(value, list):
                nested_instances[field_name] = value
            else:
                nested_data[field_name] = value
        return nested_data, nested_instances

    def _create_nested_instances(self, nested_data: Dict[str, List[Dict]], serializer: serializers.Serializer) -> Dict[str, List[Model]]:
        nested_instances = {}
        for field_name, items in nested_data.items():
            nested_field = serializer.fields[field_name]
            nested_model = nested_field.child.Meta.model
            nested_instances[field_name] = [
                nested_model.objects.create(**item)
                for item in items
            ]
        return nested_instances

    def _update_nested_relationships(self, instance: Model, nested_instances: Dict[str, List[Model]], field_name: str):
        related_field = getattr(instance, field_name)
        related_field.set(nested_instances)

    def _handle_instance_creation(self, key: str, data: Dict[str, Any]) -> Model:
        model_class, serializer = self._get_model_and_serializer(key)
        if 'user' not in data:
            raise serializers.ValidationError(f"User field missing for {key}")
        if isinstance(data, dict) and any(isinstance(v, list) for v in data.values()):
            nested_data, nested_fields = self._handle_nested_data(data)
            instance = model_class.objects.create(**nested_data)
            nested_instances = self._create_nested_instances(nested_fields, serializer)
            for field_name, related_instances in nested_instances.items():
                self._update_nested_relationships(instance, related_instances, field_name)
            return instance
        return model_class.objects.create(**data)

    def _handle_instance_update(self, instance: Model, data: Dict[str, Any], serializer: serializers.Serializer):
        if isinstance(data, dict) and any(isinstance(v, list) for v in data.values()):
            regular_data, nested_fields = self._handle_nested_data(data)
            for field_name, value in regular_data.items():
                setattr(instance, field_name, value)
            for field_name, items in nested_fields.items():
                related_field = getattr(instance, field_name)
                related_field.all().delete()
                nested_field = serializer.fields[field_name]
                nested_model = nested_field.child.Meta.model
                new_instances = [nested_model.objects.create(**item) for item in items]
                related_field.set(new_instances)
            instance.save()
        else:
            for attr, value in data.items():
                setattr(instance, attr, value)
            instance.save()

    @transaction.atomic
    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Model]:
        instances = {}
        try:
            for key, data in validated_data.items():
                if data:
                    instances[key] = self._handle_instance_creation(key, data)
            return instances
        except Exception as e:
            raise serializers.ValidationError({
                'error': f"Creation failed: {str(e)}",
                'field': key
            })

    @transaction.atomic
    def update(self, instance_mapping: Dict[str, Model], validated_data: Dict[str, Any]) -> Dict[str, Model]:
        try:
            updated_instances = {}
            for key, data in validated_data.items():
                if not data:
                    continue
                instance = instance_mapping.get(key)
                model_class, serializer = self._get_model_and_serializer(key)
                if instance:
                    self._handle_instance_update(instance, data, serializer)
                    updated_instances[key] = instance
                else:
                    updated_instances[key] = self._handle_instance_creation(key, data)
            return updated_instances
        except Exception as e:
            raise serializers.ValidationError({
                'error': f"Update failed: {str(e)}",
                'field': key
            })