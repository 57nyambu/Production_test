from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

from .models import (CompanyInformation,
                     WorkingCapital,
                     RevenueDrivers,
                     CostStracture,
                     AllExpenses,
                     Capex,
                     DividendPolicy,
                     IndustryMetrics,
                     HistoricalFinData)

from .serializers.simple import (
        CompanyInformationSerializer,
        WorkingCapitalSerializer,
        RevenueDriversSerializer,
        CostStractureSerializer,
        AllExpensesSerializer,
        CapexSerializer,
        DividendPolicySerializer,
        IndustryMetricsSerializer,
        HistoricalFinDataSerializer
    )

class SmartModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            # Check existing by unique fields within user's scope
            unique_fields = {
                field: request.data.get(field)
                for fields in self.get_queryset().model._meta.unique_together or []
                for field in fields
                if field != 'user' and request.data.get(field)
            }
            
            if unique_fields:
                instance = self.get_queryset().filter(**unique_fields).select_for_update().get()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
                
        except ObjectDoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CompanyInformationViewSet(SmartModelViewSet):
    serializer_class = CompanyInformationSerializer
    queryset = CompanyInformation.objects.all()

class WorkingCapitalViewSet(SmartModelViewSet):
    serializer_class = WorkingCapitalSerializer
    queryset = WorkingCapital.objects.all()

class RevenueDriversViewSet(SmartModelViewSet):
    serializer_class = RevenueDriversSerializer
    queryset = RevenueDrivers.objects.all()

class CostStractureViewSet(SmartModelViewSet):
    serializer_class = CostStractureSerializer
    queryset = CostStracture.objects.all()

class AllExpensesViewSet(SmartModelViewSet):
    serializer_class = AllExpensesSerializer
    queryset = AllExpenses.objects.all()

class CapexViewSet(SmartModelViewSet):
    serializer_class = CapexSerializer
    queryset = Capex.objects.all()

class DividendPolicyViewSet(SmartModelViewSet):
    serializer_class = DividendPolicySerializer
    queryset = DividendPolicy.objects.all()

class IndustryMetricsViewSet(SmartModelViewSet):
    serializer_class = IndustryMetricsSerializer
    queryset = IndustryMetrics.objects.all()

class HistoricalFinDataViewSet(SmartModelViewSet):
    serializer_class = HistoricalFinDataSerializer
    queryset = HistoricalFinData.objects.all()
    