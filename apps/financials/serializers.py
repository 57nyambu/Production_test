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
        fields = ['id', 'created_at', 'updated_at']  # Changed to list instead of tuple
        read_only_fields = ['id', 'created_at', 'updated_at']

    def _inject_user(self, validated_data):
        """Inject the authenticated user into the validated data."""
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            raise ValidationError("User must be authenticated to perform this action.")
        validated_data['user'] = current_user
        return validated_data

    def create(self, validated_data):
        """Override create method to inject the user."""
        validated_data = self._inject_user(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Override update method to inject the user."""
        validated_data = self._inject_user(validated_data)
        return super().update(instance, validated_data)


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
    #required_fields = ['average_selling_price', 'units_sold',]
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
    #required_fields = ['average_selling_price', 'units_sold']
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
    #required_fields = ['maintenance_capex', 'growth_capex', 'asset_lifespan', 'capitalized_costs']
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
        self._propagate_context(kwargs.get('context', {}))

    def _propagate_context(self, context):
        """Propagate context to nested serializers."""
        for field in self.fields.values():
            if isinstance(field, serializers.BaseSerializer):
                field.context.update(context)

    def _inject_user(self, data):
        """Inject user into data structure recursively."""
        if not self.context.get('request'):
            raise serializers.ValidationError("Request context is required")
            
        user = self.context['request'].user
        if user.is_anonymous:
            raise serializers.ValidationError("Authentication required")

        def inject_user_recursive(data_dict):
            if isinstance(data_dict, dict):
                data_dict['user'] = user
                for value in data_dict.values():
                    if isinstance(value, (dict, list)):
                        inject_user_recursive(value)
            elif isinstance(data_dict, list):
                for item in data_dict:
                    if isinstance(item, (dict, list)):
                        inject_user_recursive(item)
            return data_dict

        return inject_user_recursive(data.copy())  # Work on a copy to prevent modifying original data

    def to_internal_value(self, data):
        """Convert and validate input data."""
        validated_data = super().to_internal_value(data)
        return self._inject_user(validated_data)

    def _get_model_and_serializer(self, key):
        """Get model class and serializer instance."""
        serializer = self.fields[key]
        if hasattr(serializer, 'child'):
            model_class = serializer.child.Meta.model
        else:
            model_class = serializer.Meta.model
        return model_class, serializer

    def _handle_nested_data(self, data):
        """Split data into regular and nested fields."""
        regular_data = {}
        nested_data = {}
        
        for field_name, value in data.items():
            if isinstance(value, list):
                nested_data[field_name] = value
            elif field_name != 'user':  # Preserve user field
                regular_data[field_name] = value
                
        if 'user' in data:
            regular_data['user'] = data['user']
            
        return regular_data, nested_data

    def _create_nested_instances(self, nested_data, model_class, user):
        """Create nested model instances."""
        instances = []
        for item in nested_data:
            item['user'] = user
            instances.append(model_class.objects.create(**item))
        return instances

    @transaction.atomic
    def create(self, validated_data):
        """Create main and nested instances."""
        instances = {}
        try:
            user = self.context['request'].user
            
            for key, data in validated_data.items():
                if not data:
                    continue
                    
                model_class, serializer = self._get_model_and_serializer(key)
                regular_data, nested_data = self._handle_nested_data(data)
                
                # Create main instance
                instance = model_class.objects.create(**regular_data)
                
                # Handle nested relationships
                for field_name, items in nested_data.items():
                    nested_model = serializer.fields[field_name].child.Meta.model
                    related_instances = self._create_nested_instances(items, nested_model, user)
                    getattr(instance, field_name).set(related_instances)
                
                instances[key] = instance
                
            return instances
            
        except Exception as e:
            raise serializers.ValidationError(f"Creation failed: {str(e)}")

    @transaction.atomic
    def update(self, instance_mapping, validated_data):
        """Update main and nested instances."""
        updated_instances = {}
        try:
            user = self.context['request'].user
            
            for key, data in validated_data.items():
                if not data:
                    continue
                    
                instance = instance_mapping.get(key)
                if not instance:
                    continue
                    
                model_class, serializer = self._get_model_and_serializer(key)
                regular_data, nested_data = self._handle_nested_data(data)
                
                # Update regular fields
                for field_name, value in regular_data.items():
                    if field_name != 'user':  # Prevent user modification
                        setattr(instance, field_name, value)
                
                # Update nested relationships
                for field_name, items in nested_data.items():
                    related_field = getattr(instance, field_name)
                    related_field.all().delete()  # Clear existing relations
                    
                    nested_model = serializer.fields[field_name].child.Meta.model
                    related_instances = self._create_nested_instances(items, nested_model, user)
                    related_field.set(related_instances)
                
                instance.save()
                updated_instances[key] = instance
                
            return updated_instances
            
        except Exception as e:
            raise serializers.ValidationError(f"Update failed: {str(e)}")
