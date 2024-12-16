from rest_framework import generics, status
from rest_framework.response import Response
from .models import (
    RevenueExpenses, WorkingCapital, IndustryMetrics, 
    EmployeeSalaryInfo, CapitalExpenditure
)
from .serializers import (
    RevenueExpensesCreateSerializer, RevenueExpensesUpdateSerializer,
    WorkingCapitalCreateSerializer, WorkingCapitalUpdateSerializer,
    IndustryMetricsCreateSerializer, IndustryMetricsUpdateSerializer,
    EmployeeSalaryInfoCreateSerializer, EmployeeSalaryInfoUpdateSerializer,
    CapitalExpenditureCreateSerializer, CapitalExpenditureUpdateSerializer
)

class BaseCreateAPIView(generics.CreateAPIView):
    """
    A base class for CreateAPIView that standardizes the response format.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Data saved successfully.",
                    "data": {
                        "modelId": str(instance.id),  # Unique model identifier
                        **serializer.data,           # All saved data
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Failed to save data.",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class BaseUpdateAPIView(generics.UpdateAPIView):
    """
    A base class for UpdateAPIView that standardizes the response format.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {
                    "success": True,
                    "message": "Data updated successfully.",
                    "data": serializer.data,  # Updated data
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Failed to update data.",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# RevenueExpenses Views
class RevenueExpensesCreateView(BaseCreateAPIView):
    queryset = RevenueExpenses.objects.all()
    serializer_class = RevenueExpensesCreateSerializer

class RevenueExpensesUpdateView(BaseUpdateAPIView):
    queryset = RevenueExpenses.objects.all()
    serializer_class = RevenueExpensesUpdateSerializer

# WorkingCapital Views
class WorkingCapitalCreateView(BaseCreateAPIView):
    queryset = WorkingCapital.objects.all()
    serializer_class = WorkingCapitalCreateSerializer

class WorkingCapitalUpdateView(BaseUpdateAPIView):
    queryset = WorkingCapital.objects.all()
    serializer_class = WorkingCapitalUpdateSerializer

# IndustryMetrics Views
class IndustryMetricsCreateView(BaseCreateAPIView):
    queryset = IndustryMetrics.objects.all()
    serializer_class = IndustryMetricsCreateSerializer

class IndustryMetricsUpdateView(BaseUpdateAPIView):
    queryset = IndustryMetrics.objects.all()
    serializer_class = IndustryMetricsUpdateSerializer

# EmployeeSalaryInfo Views
class EmployeeSalaryInfoCreateView(BaseCreateAPIView):
    queryset = EmployeeSalaryInfo.objects.all()
    serializer_class = EmployeeSalaryInfoCreateSerializer

class EmployeeSalaryInfoUpdateView(BaseUpdateAPIView):
    queryset = EmployeeSalaryInfo.objects.all()
    serializer_class = EmployeeSalaryInfoUpdateSerializer

# CapitalExpenditure Views
class CapitalExpenditureCreateView(BaseCreateAPIView):
    queryset = CapitalExpenditure.objects.all()
    serializer_class = CapitalExpenditureCreateSerializer

class CapitalExpenditureUpdateView(BaseUpdateAPIView):
    queryset = CapitalExpenditure.objects.all()
    serializer_class = CapitalExpenditureUpdateSerializer
