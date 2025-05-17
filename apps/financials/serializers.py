from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (
    CompanyInformation, WorkingCapital, RevenueStream, RevenueDrivers,
    CostStracture, EmployeeInfo, AdminMarketingExp, AllExpenses,
    Asset, Capex, DividendPolicy, IndustryMetrics,HistoricalFinData, 
)
from apps.utils.baseSerializers import BaseCombinedSerializer
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

class CompanyInformationSerializer(BaseCombinedSerializer):
    fiscal_year_end = serializers.DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])
    class Meta(BaseCombinedSerializer.Meta):
        model = CompanyInformation
        fields = BaseCombinedSerializer.Meta.fields + [
            'company_name', 'industry', 'company_stage', 'funding_type', 'fiscal_year_end'
        ]


class WorkingCapitalSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = WorkingCapital
        fields = BaseCombinedSerializer.Meta.fields + [
            'days_receivables', 'days_inventory', 'days_payables', 'working_capital_days'
        ]


class RevenueStreamSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = RevenueStream
        fields = BaseCombinedSerializer.Meta.fields + [
            'name', 'type', 'amount'#, 'percentage'
        ]


class RevenueDriversSerializer(BaseCombinedSerializer):
    #required_fields = ['average_selling_price', 'units_sold',]
    revenue_streams = RevenueStreamSerializer(many=True, required=False)

    class Meta(BaseCombinedSerializer.Meta):
        model = RevenueDrivers
        fields = BaseCombinedSerializer.Meta.fields + [
            'percentage_comm', 'units_sold', 'revenue_streams', 'q1', 'q2', 'q3', 'q4'
        ]


class CostStractureSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = CostStracture
        fields = BaseCombinedSerializer.Meta.fields + [
            'raw_material', 'direct_labor', 'man_overhead', 'total_cogs',
            'fixed_cost', 'variable_cost', 'cd_raw_material', 'cd_direct_labor', 'cd_man_overhead'
        ]


class EmployeeInfoSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = EmployeeInfo
        fields = BaseCombinedSerializer.Meta.fields + [
            'position', 'salary', 'count', 'salary_growth_rate'
        ]


class AdminMarketingExpSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = AdminMarketingExp
        fields = BaseCombinedSerializer.Meta.fields + [
            'exp_type', 'amount', 'description'
        ]


class AllExpensesSerializer(BaseCombinedSerializer):
    employee_info = EmployeeInfoSerializer(many=True, required=False)
    admin_marketing_exp = AdminMarketingExpSerializer(many=True, required=False)

    class Meta(BaseCombinedSerializer.Meta):
        model = AllExpenses
        fields = BaseCombinedSerializer.Meta.fields + [
            'employee_info', 'salary_growth_rate', 'admin_marketing_exp'
        ]


class AssetSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = Asset
        fields = BaseCombinedSerializer.Meta.fields + [
            'name', 'value', 'type', 'description'
        ]


class CapexSerializer(BaseCombinedSerializer):
    assets = AssetSerializer(many=True, required=False)

    class Meta(BaseCombinedSerializer.Meta):
        model = Capex
        fields = BaseCombinedSerializer.Meta.fields + [
            'maintenance_capex', 'growth_capex', 'asset_lifespan', 'capitalized_costs', 'assets'
        ]


class DividendPolicySerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = DividendPolicy
        fields = BaseCombinedSerializer.Meta.fields + [
            'payout_ratio', 'div_per_share', 'div_growth_rt'
        ]


class IndustryMetricsSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = IndustryMetrics
        fields = BaseCombinedSerializer.Meta.fields + [
            'market_share', 'industry_growth_rate', 'competitor_count', 'market_size',
            'corporate_tax_rate', 'inflation_rate', 'gdp_growth_rate', 'interest_rate'
        ]


class HistoricalFinDataSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = HistoricalFinData
        fields = BaseCombinedSerializer.Meta.fields + [
            'revenue', 'cogs', 'salaries', 'rent', 'marketing', 'technology', 
            'insurance', 'other', 'total_operating_expenses', 'cash_equivs', 
            'acc_receivable', 'inventory', 'fixed_assets', 'acc_payable', 
            'short_debt', 'long_debt', 'paid_in_cap', 'retained_earning'
        ]

#combined serializer 

