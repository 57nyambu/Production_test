from rest_framework import serializers
from apps.financials.models import (
    RevenueDrivers, 
    CostStracture, 
    AllExpenses
)
from apps.financials.serializers import (
    RevenueDriversSerializer,
    CostStractureSerializer,
    AllExpensesSerializer
)


class OutPutSerializer(serializers.Serializer):
    revenue_drivers = RevenueDriversSerializer(many=True, required=False)
    cost_structure = CostStractureSerializer(many=True, required=False)
    all_expenses = AllExpensesSerializer(many=True, required=False)

    