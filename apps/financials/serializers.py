from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
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
        fields = ['id', 'created_at', 'updated_at']


class CompanyInformationSerializer(BaseModelSerializer):
    fiscal_year_end = serializers.DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])
    class Meta:
        model = CompanyInformation
        fields = BaseModelSerializer.Meta.fields + [
            'company_name', 'industry', 'company_stage', 'funding_type', 'fiscal_year_end'
        ]


class WorkingCapitalSerializer(BaseModelSerializer):
    class Meta:
        model = WorkingCapital
        fields = BaseModelSerializer.Meta.fields + [
            'days_receivables', 'days_inventory', 'days_payables', 'working_capital_days'
        ]


class RevenueStreamSerializer(BaseModelSerializer):
    class Meta:
        model = RevenueStream
        fields = BaseModelSerializer.Meta.fields + [
            'name', 'type', 'amount'
        ]


class RevenueDriversSerializer(RequiredFieldsMixin, BaseModelSerializer):
    required_fields = ['average_selling_price', 'units_sold',]
    revenue_streams = RevenueStreamSerializer(many=True, required=False)

    class Meta:
        model = RevenueDrivers
        fields = BaseModelSerializer.Meta.fields + [
            'average_selling_price', 'units_sold', 'revenue_streams'
        ]


class CostStractureSerializer(BaseModelSerializer):
    class Meta:
        model = CostStracture
        fields = BaseModelSerializer.Meta.fields + [
            'raw_material', 'direct_labor', 'man_overhead', 'total_cogs',
            'fixed_cost', 'variable_cost', 'cd_raw_material', 'cd_direct_labor', 'cd_man_overhead'
        ]


class EmployeeInfoSerializer(BaseModelSerializer):
    class Meta:
        model = EmployeeInfo
        fields = BaseModelSerializer.Meta.fields + [
            'position', 'salary', 'count', 'salary_growth_rate'
        ]


class AdminMarketingExpSerializer(BaseModelSerializer):
    class Meta:
        model = AdminMarketingExp
        fields = BaseModelSerializer.Meta.fields + [
            'exp_type', 'amount', 'description'
        ]


class AllExpensesSerializer(RequiredFieldsMixin ,BaseModelSerializer):
    required_fields = ['average_selling_price', 'units_sold']
    employee_info = EmployeeInfoSerializer(many=True, required=False)
    admin_marketing_exp = AdminMarketingExpSerializer(many=True, required=False)

    class Meta:
        model = AllExpenses
        fields = BaseModelSerializer.Meta.fields + [
            'employee_info', 'average_selling_price', 'units_sold', 'admin_marketing_exp'
        ]

class AssetSerializer(BaseModelSerializer):
    class Meta:
        model = Asset
        fields = BaseModelSerializer.Meta.fields + [
            'name', 'value', 'type', 'description'
        ]


class CapexSerializer(RequiredFieldsMixin, BaseModelSerializer):
    required_fields = ['maintenance_capex', 'growth_capex', 'asset_lifespan', 'capitalized_costs']
    assets = AssetSerializer(many=True, required=False)

    class Meta:
        model = Capex
        fields = BaseModelSerializer.Meta.fields + [
            'maintenance_capex', 'growth_capex', 'asset_lifespan', 'capitalized_costs', 'assets'
        ]


class DividendPolicySerializer(BaseModelSerializer):
    class Meta:
        model = DividendPolicy
        fields = BaseModelSerializer.Meta.fields + [
            'payout_ratio', 'div_per_share', 'div_growth_rt'
        ]


class IndustryMetricsSerializer(BaseModelSerializer):
    class Meta:
        model = IndustryMetrics
        fields = BaseModelSerializer.Meta.fields + [
            'market_share', 'industry_growth_rate', 'competitor_count', 'market_size',
            'corporate_tax_rate', 'inflation_rate', 'gdp_growth_rate', 'interest_rate'
        ]


class HistoricalFinDataSerializer(BaseModelSerializer):
    class Meta:
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

    def create(self, validated_data):
        instances = {}
        with transaction.atomic():
            for key, data in validated_data.items():
                if data:
                    try:
                        serializer = self.fields[key]
                        # Get the model class from child serializer if it's a ListSerializer
                        if hasattr(serializer, 'child'):
                            model_class = serializer.child.Meta.model
                        else:
                            model_class = serializer.Meta.model

                        # Handle nested serializers (like revenue_streams)
                        if isinstance(data, dict) and any(isinstance(v, list) for v in data.values()):
                            nested_data = {}
                            nested_instances = {}
                            
                            # Separate nested lists from regular fields
                            for field_name, value in data.items():
                                if isinstance(value, list):
                                    nested_field = serializer.fields[field_name]
                                    nested_model = nested_field.child.Meta.model
                                    nested_instances[field_name] = [
                                        nested_model.objects.create(**item)
                                        for item in value
                                    ]
                                else:
                                    nested_data[field_name] = value

                            # Create main instance
                            instance = model_class.objects.create(**nested_data)
                            
                            # Set relationships
                            for field_name, related_instances in nested_instances.items():
                                related_field = getattr(instance, field_name)
                                related_field.set(related_instances)
                            
                            instances[key] = instance
                        else:
                            # Handle regular models without nested relationships
                            instances[key] = model_class.objects.create(**data)
                            
                    except Exception as e:
                        raise serializers.ValidationError({key: str(e)})
        return instances

    def update(self, instance_mapping, validated_data):
        with transaction.atomic():
            updated_instances = {}
            for key, data in validated_data.items():
                if data:
                    try:
                        serializer = self.fields[key]
                        instance = instance_mapping.get(key)
                        # Get the model class from child serializer if it's a ListSerializer
                        if hasattr(serializer, 'child'):
                            model_class = serializer.child.Meta.model
                        else:
                            model_class = serializer.Meta.model

                        if isinstance(data, dict) and any(isinstance(v, list) for v in data.values()):
                            # Handle models with nested relationships
                            if instance:
                                # Update regular fields
                                for field_name, value in data.items():
                                    if not isinstance(value, list):
                                        setattr(instance, field_name, value)
                                
                                # Update nested relationships
                                for field_name, value in data.items():
                                    if isinstance(value, list):
                                        related_field = getattr(instance, field_name)
                                        related_field.all().delete()
                                        
                                        nested_field = serializer.fields[field_name]
                                        nested_model = nested_field.child.Meta.model
                                        new_instances = [
                                            nested_model.objects.create(**item)
                                            for item in value
                                        ]
                                        related_field.set(new_instances)
                                
                                instance.save()
                                updated_instances[key] = instance
                            else:
                                updated_instances[key] = self.create({key: data})[key]
                        else:
                            # Handle regular models
                            if instance:
                                for attr, value in data.items():
                                    setattr(instance, attr, value)
                                instance.save()
                                updated_instances[key] = instance
                            else:
                                updated_instances[key] = model_class.objects.create(**data)
                                
                    except Exception as e:
                        raise serializers.ValidationError({key: str(e)})
        return updated_instances

