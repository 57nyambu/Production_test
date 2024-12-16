from rest_framework import serializers
from .models import (
    RevenueExpenses, WorkingCapital, IndustryMetrics, 
    EmployeeSalaryInfo, Staff, AdminExpense, 
    CapitalExpenditure, CapitalAsset
)

# CREATE SERIALIZERS

class RevenueExpensesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueExpenses
        fields = [
            'revenue', 'expenses', 'cost_of_goods_sold', 'direct_labor', 
            'manufacturing_overhead', 'gross_profit', 
            'salaries', 'rent', 'marketing', 'technology', 
            'insurance', 'other', 'total_operating_expenses'
        ]

# WorkingCapital Create Serializer
class WorkingCapitalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingCapital
        fields = '__all__'

# IndustryMetrics Create Serializer
class IndustryMetricsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryMetrics
        fields = '__all__'

# EmployeeSalaryInfo Create Serializer
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class AdminExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminExpense
        fields = '__all__'

class EmployeeSalaryInfoCreateSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(many=True, required=False)
    admin_expenses = AdminExpenseSerializer(many=True, required=False)

    class Meta:
        model = EmployeeSalaryInfo
        fields = ['salary_growth', 'staff', 'admin_expenses']

    def create(self, validated_data):
        staff_data = validated_data.pop('staff', [])
        admin_expenses_data = validated_data.pop('admin_expenses', [])
        employee_salary_info = EmployeeSalaryInfo.objects.create(**validated_data)

        for staff in staff_data:
            Staff.objects.create(employee_salary_info=employee_salary_info, **staff)

        for expense in admin_expenses_data:
            AdminExpense.objects.create(employee_salary_info=employee_salary_info, **expense)

        return employee_salary_info

# CapitalExpenditure Create Serializer
class CapitalAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapitalAsset
        fields = '__all__'

class CapitalExpenditureCreateSerializer(serializers.ModelSerializer):
    capital_assets = CapitalAssetSerializer(many=True, required=False)

    class Meta:
        model = CapitalExpenditure
        fields = ['maintenance_capex', 'growth_capex', 'asset_lifespan', 'capitalized_costs', 'capital_assets']

    def create(self, validated_data):
        assets_data = validated_data.pop('capital_assets', [])
        capex = CapitalExpenditure.objects.create(**validated_data)

        for asset in assets_data:
            CapitalAsset.objects.create(capital_expenditure=capex, **asset)

        return capex

# UPDATE SERIALIZERS

# RevenueExpenses Update Serializer
class RevenueExpensesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueExpenses
        fields = '__all__'
        extra_kwargs = {
            field: {'required': False} for field in fields
        }

# WorkingCapital Update Serializer
class WorkingCapitalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingCapital
        fields = '__all__'
        extra_kwargs = {
            field: {'required': False} for field in fields
        }

# IndustryMetrics Update Serializer
class IndustryMetricsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryMetrics
        fields = '__all__'
        extra_kwargs = {
            field: {'required': False} for field in fields
        }

# EmployeeSalaryInfo Update Serializer
class EmployeeSalaryInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSalaryInfo
        fields = '__all__'
        extra_kwargs = {
            field: {'required': False} for field in fields
        }

# CapitalExpenditure Update Serializer
class CapitalExpenditureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapitalExpenditure
        fields = '__all__'
        extra_kwargs = {
            field: {'required': False} for field in fields
        }
