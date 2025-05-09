from rest_framework import serializers
from apps.financials.models import (
    RevenueDrivers, 
    CostStracture, 
    AllExpenses
)

class RevenueOutputSerializer(serializers.Serializer):
    revenue = serializers.DecimalField(max_digits=20, decimal_places=2)
    cogs = serializers.DecimalField(max_digits=20, decimal_places=2)
    gross_profit = serializers.DecimalField(max_digits=20, decimal_places=2)
    gross_mirgin = serializers.DecimalField(max_digits=20, decimal_places=2)


class AllExpensesOutputSerializer(serializers.Serializer):
    sales_exp = serializers.DecimalField(max_digits=20, decimal_places=2)
    marketing_exp = serializers.DecimalField(max_digits=20, decimal_places=2)
    research_dev = serializers.DecimalField(max_digits=20, decimal_places=2)
    gen_admin = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_exp = serializers.DecimalField(max_digits=20, decimal_places=2)


class OperationEbitdaSerializer(serializers.Serializer):
    operating_income = serializers.DecimalField(max_digits=20, decimal_places=2)
    depriciation = serializers.DecimalField(max_digits=20, decimal_places=2)
    armotization = serializers.DecimalField(max_digits=20, decimal_places=2)
    ebit = serializers.DecimalField(max_digits=20, decimal_places=2)


class NetIncomeSerializer(serializers.Serializer):
    interest_exp = serializers.DecimalField(max_digits=20, decimal_places=2)
    pretax_income = serializers.DecimalField(max_digits=20, decimal_places=2)
    tax = serializers.DecimalField(max_digits=20, decimal_places=2)
    net_income = serializers.DecimalField(max_digits=20, decimal_places=2)


class CombinedOutputSerializer(serializers.Serializer):
    revenue = RevenueOutputSerializer()
    expenses = AllExpensesOutputSerializer()
    operations = OperationEbitdaSerializer()
    netincome = NetIncomeSerializer()