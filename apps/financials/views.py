from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

class BaseModelAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch']
    
    ERROR_MESSAGES = {
        'not_found': "Resource not found.",
        'server_error': "An unexpected error occurred.",
        'validation_error': "Invalid data provided.",
        'success_get': "Data retrieved successfully.",
        'success_create': "Data created successfully.",
        'success_update': "Data updated successfully."
    }

    def get_queryset(self):
        """Get queryset filtered by current user."""
        return self.serializer_class.Meta.model.objects.filter(user=self.request.user)

    def create_response(self, success, message, data=None, status_code=status.HTTP_200_OK):
        """Create standardized response."""
        response_data = {
            'success': success,
            'message': message
        }
        if data is not None:
            response_data['data'] = data
        return Response(response_data, status=status_code)

    def get(self, request, *args, **kwargs):
        """Retrieve user's data."""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset.first())
            return self.create_response(
                True,
                self.ERROR_MESSAGES['success_get'],
                serializer.data
            )
        except Exception as e:
            return self.create_response(
                False,
                f"{self.ERROR_MESSAGES['server_error']}: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Create new instance."""
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return self.create_response(
                    False,
                    self.ERROR_MESSAGES['validation_error'],
                    serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            instance = serializer.save()
            return self.create_response(
                True,
                self.ERROR_MESSAGES['success_create'],
                serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return self.create_response(
                False,
                f"{self.ERROR_MESSAGES['server_error']}: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        """Full update of instance."""
        try:
            instance = self.get_queryset().first()
            if not instance:
                return self.create_response(
                    False,
                    self.ERROR_MESSAGES['not_found'],
                    status_code=status.HTTP_404_NOT_FOUND
                )

            serializer = self.get_serializer(instance, data=request.data)
            if not serializer.is_valid():
                return self.create_response(
                    False,
                    self.ERROR_MESSAGES['validation_error'],
                    serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            instance = serializer.save()
            return self.create_response(
                True,
                self.ERROR_MESSAGES['success_update'],
                serializer.data
            )
        except Exception as e:
            return self.create_response(
                False,
                f"{self.ERROR_MESSAGES['server_error']}: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        """Partial update of instance."""
        try:
            instance = self.get_queryset().first()
            if not instance:
                return self.create_response(
                    False,
                    self.ERROR_MESSAGES['not_found'],
                    status_code=status.HTTP_404_NOT_FOUND
                )

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if not serializer.is_valid():
                return self.create_response(
                    False,
                    self.ERROR_MESSAGES['validation_error'],
                    serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            instance = serializer.save()
            return self.create_response(
                True,
                self.ERROR_MESSAGES['success_update'],
                serializer.data
            )
        except Exception as e:
            return self.create_response(
                False,
                f"{self.ERROR_MESSAGES['server_error']}: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# Individual views inheriting from BaseModelAPIView
class CompanyInformationAPIView(BaseModelAPIView):
    serializer_class = CompanyInformationSerializer
    model = CompanyInformation

class WorkingCapitalAPIView(BaseModelAPIView):
    serializer_class = WorkingCapitalSerializer
    model = WorkingCapital

class RevenueDriversAPIView(BaseModelAPIView):
    serializer_class = RevenueDriversSerializer
    model = RevenueDrivers

class CostStractureAPIView(BaseModelAPIView):
    serializer_class = CostStractureSerializer
    model = CostStracture

class AllExpensesAPIView(BaseModelAPIView):
    serializer_class = AllExpensesSerializer
    model = AllExpenses

class CapexAPIView(BaseModelAPIView):
    serializer_class = CapexSerializer
    model = Capex

class DividendPolicyAPIView(BaseModelAPIView):
    serializer_class = DividendPolicySerializer
    model = DividendPolicy

class IndustryMetricsAPIView(BaseModelAPIView):
    serializer_class = IndustryMetricsSerializer
    model = IndustryMetrics

class HistoricalFinDataAPIView(BaseModelAPIView):
    serializer_class = HistoricalFinDataSerializer
    model = HistoricalFinData
