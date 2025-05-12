from .models import CustomerModel
from apps.marketing.models import GrowthRate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (
    CustomerModelSerializer,
    CombinedCustomerMetricsSerializer,
    CustomerDistributionSerializer,
)
from .services import get_combined_customer_metrics
from apps.utils.baseViews import BaseAPIView

class CustomerModelView(BaseAPIView):
    model = CustomerModel
    serializer_class = CustomerModelSerializer


class CombinedCustomerMetricsView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        data, error = get_combined_customer_metrics(request.user)
        if error:
            return Response({"success": False, "message": error}, status=status.HTTP_404_NOT_FOUND)
        serializer = CombinedCustomerMetricsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True, "data": serializer.data})