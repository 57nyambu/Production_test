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
import logging

# Don't even think about touching it, validating req fields
logger = logging.getLogger(__name__)

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

    def get_fields(self):
        fields = super().get_fields()
        if self.context.get('nested_depth', 0) > 10:
            return {}
        return fields

    @transaction.atomic
    def create(self, validated_data):
        """
        Handle creation with nested relationships
        """
        nested_fields = self._get_nested_fields()
        nested_data = {}

        # Extract nested data from validated_data
        for field_name in nested_fields:
            if field_name in validated_data:
                nested_data[field_name] = validated_data.pop(field_name)

        # Create the main instance
        validated_data['user'] = self.context['request'].user
        instance = super().create(validated_data)

        # Handle nested creates
        self._handle_nested_operations(instance, nested_data, create=True)

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Handle updates with nested relationships
        """
        nested_fields = self._get_nested_fields()
        nested_data = {}

        # Extract nested data from validated_data
        for field_name in nested_fields:
            if field_name in validated_data:
                nested_data[field_name] = validated_data.pop(field_name)

        # Update the main instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle nested updates
        self._handle_nested_operations(instance, nested_data, create=False)

        return instance

    def _get_nested_fields(self):
        """
        Get all nested serializer fields
        """
        nested_fields = []
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.BaseSerializer) and not field.read_only:
                nested_fields.append(field_name)
        return nested_fields

    def _handle_nested_operations(self, instance, nested_data, create=False):
        """
        Handle nested create/update operations
        """
        for field_name, field_data in nested_data.items():
            field = self.fields[field_name]
            field.context['nested_depth'] = self.context.get('nested_depth', 0) + 1
            field.context['request'] = self.context.get('request')

            if isinstance(field_data, list):
                self._handle_many_nested(instance, field_name, field_data, field, create)
            else:
                self._handle_single_nested(instance, field_name, field_data, field, create)

    def _handle_single_nested(self, instance, field_name, field_data, field, create):
        """
        Handle single nested relationship
        """
        if field_data is None:
            return

        related_instance = getattr(instance, field_name, None)
        
        if create or not related_instance:
            # Create new related instance
            field_data['user'] = instance.user
            serializer = field.__class__(data=field_data, context=field.context)
            serializer.is_valid(raise_exception=True)
            related_instance = serializer.save()
            setattr(instance, field_name, related_instance)
            instance.save()
        else:
            # Update existing related instance
            serializer = field.__class__(
                related_instance,
                data=field_data,
                partial=True,
                context=field.context
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def _handle_many_nested(self, instance, field_name, field_data, field, create):
        """
        Handle many-to-many or one-to-many relationships
        """
        related_field = getattr(instance, field_name)
        
        if create:
            # Create new related instances
            serializer = field.__class__(
                data=field_data,
                many=True,
                context=field.context
            )
            serializer.is_valid(raise_exception=True)
            related_instances = serializer.save()
            if isinstance(related_field, models.Manager):
                related_field.set(related_instances)
            else:
                setattr(instance, field_name, related_instances)
            instance.save()
        else:
            # Update existing related instances
            existing_instances = {
                str(item.id): item 
                for item in related_field.all()
            }
            
            to_create = []
            to_update = []
            
            for item_data in field_data:
                item_id = str(item_data.get('id', ''))
                if item_id and item_id in existing_instances:
                    to_update.append((existing_instances[item_id], item_data))
                else:
                    to_create.append(item_data)

            # Handle updates
            for existing, update_data in to_update:
                serializer = field.__class__(
                    existing,
                    data=update_data,
                    partial=True,
                    context=field.context
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

            # Handle creates
            if to_create:
                serializer = field.__class__(
                    data=to_create,
                    many=True,
                    context=field.context
                )
                serializer.is_valid(raise_exception=True)
                new_instances = serializer.save()
                
                if isinstance(related_field, models.Manager):
                    current = list(related_field.all())
                    related_field.set(current + list(new_instances))
                else:
                    setattr(instance, field_name, new_instances)
                instance.save()


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


class RevenueDriversSerializer(BaseModelSerializer):
    required_fields = ['average_selling_price', 'units_sold']
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


# Improved Combined Serializer
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
        for field in self.fields.values():
            if isinstance(field, serializers.BaseSerializer):
                field.context.update(context)

    def to_internal_value(self, data):
        data = self._add_user_to_nested_data(data.copy())
        return super().to_internal_value(data)

    def _add_user_to_nested_data(self, data, user_id=None):
        if user_id is None:
            user_id = self.context['request'].user.id

        if isinstance(data, dict):
            data['user'] = user_id
            return {
                key: self._add_user_to_nested_data(value, user_id)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self._add_user_to_nested_data(item, user_id) for item in data]
        return data

    def _update_nested_field(self, instance, field_name, nested_data):
        related_field = getattr(instance, field_name)
        model_class = self.fields[field_name].Meta.model

        if isinstance(nested_data, list):
            existing_items = {str(item.id): item for item in related_field.all()}
            updated_items = []
            for item_data in nested_data:
                item_id = str(item_data.get('id'))
                if item_id and item_id in existing_items:
                    item = existing_items[item_id]
                    for attr, value in item_data.items():
                        if attr != 'id':
                            setattr(item, attr, value)
                    item.save()
                    updated_items.append(item)
                else:
                    new_item = model_class.objects.create(**item_data)
                    updated_items.append(new_item)
            related_field.set(updated_items)
        else:
            if related_field:
                for attr, value in nested_data.items():
                    setattr(related_field, attr, value)
                related_field.save()
            else:
                new_related = model_class.objects.create(**nested_data)
                setattr(instance, field_name, new_related)
                instance.save()

    @transaction.atomic
    def create(self, validated_data):
        instances = {}
        
        for field_name, field_data in validated_data.items():
            if not field_data:
                continue

            many_to_many_fields = {}
            # Separate many-to-many field data
            for key, value in list(field_data.items()):
                if isinstance(self.fields[field_name].fields[key], serializers.ListSerializer):
                    many_to_many_fields[key] = field_data.pop(key)

            model_class = self.fields[field_name].Meta.model
            # Create the main instance
            instance = model_class.objects.create(**field_data)

            # Handle many-to-many fields
            for m2m_field, m2m_data in many_to_many_fields.items():
                related_serializer = self.fields[field_name].fields[m2m_field].child
                related_model = related_serializer.Meta.model
                related_instances = [related_model.objects.create(**item) for item in m2m_data]
                getattr(instance, m2m_field).set(related_instances)

            instances[field_name] = instance

        return instances


    @transaction.atomic
    def update(self, instance_mapping, validated_data):
        updated_instances = {}
        
        for field_name, field_data in validated_data.items():
            if not field_data:
                continue

            many_to_many_fields = {}
            # Separate many-to-many field data
            for key, value in list(field_data.items()):
                if isinstance(self.fields[field_name].fields[key], serializers.ListSerializer):
                    many_to_many_fields[key] = field_data.pop(key)

            instance = instance_mapping.get(field_name)
            if instance:
                # Update main instance
                for attr, value in field_data.items():
                    setattr(instance, attr, value)
                instance.save()

                # Update many-to-many fields
                for m2m_field, m2m_data in many_to_many_fields.items():
                    related_serializer = self.fields[field_name].fields[m2m_field].child
                    related_model = related_serializer.Meta.model
                    related_instances = [related_model.objects.create(**item) for item in m2m_data]
                    getattr(instance, m2m_field).set(related_instances)

                updated_instances[field_name] = instance

        return updated_instances
