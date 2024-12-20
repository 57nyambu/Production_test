from rest_framework import serializers
from .models import (
    CompanyInformation, WorkingCapital, RevenueStream, RevenueDrivers,
    CostStracture, EmployeeInfo, AdminMarketingExp, AllExpenses,
    Asset, Capex, DividendPolicy, IndustryMetrics,HistoricalFinData, 

)

# Serializers
class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'created_at', 'updated_at']


class CompanyInformationSerializer(BaseModelSerializer):
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


class RevenueDriversSerializer(BaseModelSerializer):
    revenue_streams = RevenueStreamSerializer(many=True)

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


class AllExpensesSerializer(BaseModelSerializer):
    employee_info = EmployeeInfoSerializer(read_only=True)
    admin_marketing_exp = AdminMarketingExpSerializer(read_only=True)

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


class CapexSerializer(BaseModelSerializer):
    assets = AssetSerializer(many=True)

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

#combined serializer for creation
from rest_framework.exceptions import ValidationError
from django.db import transaction

class CombinedSerializer(serializers.Serializer):
    company_information = CompanyInformationSerializer()
    working_capital = WorkingCapitalSerializer()
    revenue_drivers = RevenueDriversSerializer()
    cost_structure = CostStractureSerializer()
    all_expenses = AllExpensesSerializer()
    asset = AssetSerializer()
    capex = CapexSerializer()
    dividend_policy = DividendPolicySerializer()
    industry_metrics = IndustryMetricsSerializer()
    historical_fin_data = HistoricalFinDataSerializer()

    def create(self, validated_data):
        # Define the models to dynamically create instances
        model_instance_map = {
            'company_information': CompanyInformation,
            'working_capital': WorkingCapital,
            'revenue_drivers': RevenueDrivers,
            'cost_structure': CostStracture,
            'all_expenses': AllExpenses,
            'asset': Asset,
            'capex': Capex,
            'dividend_policy': DividendPolicy,
            'industry_metrics': IndustryMetrics,
            'historical_fin_data': HistoricalFinData
        }

        instance_mapping = {}
        with transaction.atomic():  # Ensure atomicity
            for key, model in model_instance_map.items():
                if key in validated_data:
                    data = validated_data.pop(key)
                    # Handle Capex serializer specifically for assets
                    if key == 'capex':
                        asset_data = validated_data.pop('asset', [])
                        if not isinstance(asset_data, list):
                            raise ValidationError("Asset data should be a list of assets.")
                        assets = []
                        for asset in asset_data:
                            if not isinstance(asset, dict):
                                raise ValidationError(f"Asset data is malformed: {asset}")
                            assets.append(Asset.objects.create(**asset))
                        data['assets'] = assets

                    # Ensure the data is in the correct format (e.g., dictionaries for models)
                    if not isinstance(data, dict):
                        raise ValidationError(f"Data for {key} is not in the correct format.")

                    try:
                        # Create the model instance
                        instance = model.objects.create(**data)
                        instance_mapping[key] = instance
                    except Exception as e:
                        raise ValidationError(f"Error creating {key}: {str(e)}")
                else:
                    raise ValidationError(f"Missing data for {key}.")
        
        return validated_data

