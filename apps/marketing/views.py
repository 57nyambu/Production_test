from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import get_growth_metrics
from .serializers import (
    MarketingMetricsSerializer,
    GrowthProjectionSerializer,
    CustomerTypeDistributionSerializer
)
from rest_framework import status

from apps.utils.baseViews import BaseAPIView
from .models import MarketingMetrics

class MarketingMetricsView(BaseAPIView):
    model = MarketingMetrics
    serializer_class = MarketingMetricsSerializer

class GrowthProjectionView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """Handle GET request for growth projections and customer distribution."""
        data, error, status_code = get_growth_metrics(request.user)
        
        if error:
            return Response(
                {"success": False, "error": error}, 
                status=status_code
            )

        try:
            # Validate and serialize the data
            growth_data = GrowthProjectionSerializer(
                data=data["growth_projection"], 
                many=True
            )
            distribution_data = CustomerTypeDistributionSerializer(
                data=data["customer_distribution"], 
                many=True
            )

            growth_data.is_valid(raise_exception=True)
            distribution_data.is_valid(raise_exception=True)

            return Response({
                "success": True,
                "data": {
                    "growth_projection": growth_data.data,
                    "customer_distribution": distribution_data.data
                }
            })

        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )