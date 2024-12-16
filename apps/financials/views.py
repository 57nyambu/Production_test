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

# RevenueExpenses Views
class RevenueExpensesCreateView(generics.CreateAPIView):
    queryset = RevenueExpenses.objects.all()
    serializer_class = RevenueExpensesCreateSerializer

class RevenueExpensesUpdateView(generics.UpdateAPIView):
    queryset = RevenueExpenses.objects.all()
    serializer_class = RevenueExpensesUpdateSerializer

# WorkingCapital Views
class WorkingCapitalCreateView(generics.CreateAPIView):
    queryset = WorkingCapital.objects.all()
    serializer_class = WorkingCapitalCreateSerializer

class WorkingCapitalUpdateView(generics.UpdateAPIView):
    queryset = WorkingCapital.objects.all()
    serializer_class = WorkingCapitalUpdateSerializer

# IndustryMetrics Views
class IndustryMetricsCreateView(generics.CreateAPIView):
    queryset = IndustryMetrics.objects.all()
    serializer_class = IndustryMetricsCreateSerializer

class IndustryMetricsUpdateView(generics.UpdateAPIView):
    queryset = IndustryMetrics.objects.all()
    serializer_class = IndustryMetricsUpdateSerializer

# EmployeeSalaryInfo Views
class EmployeeSalaryInfoCreateView(generics.CreateAPIView):
    queryset = EmployeeSalaryInfo.objects.all()
    serializer_class = EmployeeSalaryInfoCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EmployeeSalaryInfoUpdateView(generics.UpdateAPIView):
    queryset = EmployeeSalaryInfo.objects.all()
    serializer_class = EmployeeSalaryInfoUpdateSerializer

# CapitalExpenditure Views
class CapitalExpenditureCreateView(generics.CreateAPIView):
    queryset = CapitalExpenditure.objects.all()
    serializer_class = CapitalExpenditureCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CapitalExpenditureUpdateView(generics.UpdateAPIView):
    queryset = CapitalExpenditure.objects.all()
    serializer_class = CapitalExpenditureUpdateSerializer
