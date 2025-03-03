from apps.utils.baseViews import BaseAPIView
from .serializers import (
    CompanyInformationSerializer,
    WorkingCapitalSerializer,
    RevenueDriversSerializer,
    CostStractureSerializer,
    AllExpensesSerializer,
    CapexSerializer,
    DividendPolicySerializer,
    IndustryMetricsSerializer,
    HistoricalFinDataSerializer,
)
from .models import (
    CompanyInformation,
    WorkingCapital,
    RevenueDrivers,
    CostStracture,
    AllExpenses,
    Capex,
    DividendPolicy,
    IndustryMetrics,
    HistoricalFinData,
)

class CompanyInformationAPIView(BaseAPIView):
    serializer_class = CompanyInformationSerializer
    model = CompanyInformation

class WorkingCapitalAPIView(BaseAPIView):
    serializer_class = WorkingCapitalSerializer
    model = WorkingCapital

class RevenueDriversAPIView(BaseAPIView):
    serializer_class = RevenueDriversSerializer
    model = RevenueDrivers

class CostStractureAPIView(BaseAPIView):
    serializer_class = CostStractureSerializer
    model = CostStracture

class AllExpensesAPIView(BaseAPIView):
    serializer_class = AllExpensesSerializer
    model = AllExpenses

class CapexAPIView(BaseAPIView):
    serializer_class = CapexSerializer
    model = Capex

class DividendPolicyAPIView(BaseAPIView):
    serializer_class = DividendPolicySerializer
    model = DividendPolicy

class IndustryMetricsAPIView(BaseAPIView):
    serializer_class = IndustryMetricsSerializer
    model = IndustryMetrics

class HistoricalFinDataAPIView(BaseAPIView):
    serializer_class = HistoricalFinDataSerializer
    model = HistoricalFinData
