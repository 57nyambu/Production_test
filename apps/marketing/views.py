from .models import MarketingMetrics
from .serializers import (
    MarketingMetricsSerializer,
    GrowthProjectionSerializer,
    CustomerTypeDistributionSerializer,
)
from apps.financials.models import RevenueStream
from apps.utils.baseViews import BaseAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.customer.models import CustomerDistribution, CustomerModel
from rest_framework.views import APIView
from rest_framework import serializers  # For local serializer


# Local serializer for RevenueStream (only name and percentage)
class LocalRevenueStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueStream
        fields = ['name', 'percentage']


class MarketingMetricsView(BaseAPIView):
    """View to handle Marketing Metrics API requests."""
    model = MarketingMetrics
    serializer_class = MarketingMetricsSerializer


class GrowthProjectionView(APIView):
    """View to handle Growth Projection API requests."""

    def get(self, request, *args, **kwargs):
        """Handle GET request for growth projection."""
        # Fetch the MarketingMetrics instance for the current user
        instance = MarketingMetrics.objects.filter(user=request.user).first()
        if not instance:
            return self._error_response("No data found for MarketingMetrics.", status.HTTP_404_NOT_FOUND)
        
        customer_instance = CustomerModel.objects.filter(user=request.user).first()
        if not customer_instance:
            return self._error_response("No data found for CustomerModel.", status.HTTP_404_NOT_FOUND)
        
        beginning_client = customer_instance.beginning_client

        # Delegate growth projection calculation to the model
        yearly_projections = instance.calculate_growth_projections(beginning_client)
        if not yearly_projections:
            return self._error_response("No growth rates found for projection.", status.HTTP_400_BAD_REQUEST)

        # Get the customer distribution as before
        distribution_data = CustomerDistribution.calculate_distribution(request.user, yearly_projections[0]["customers"])

        # Fetch RevenueStreams for the user and serialize
        revenue_streams = RevenueStream.objects.filter(user=request.user)
        revenue_data = LocalRevenueStreamSerializer(revenue_streams, many=True).data

        # Replace 'customer_type' and 'percentage' in distribution_data with values from RevenueStream
        # Match by index, up to the shortest list
        min_len = min(len(distribution_data), len(revenue_data))
        for i in range(min_len):
            distribution_data[i]["customer_type"] = revenue_data[i]["name"]
            distribution_data[i]["percentage"] = revenue_data[i]["percentage"]

        # Optionally, if distribution_data is longer, clear out the unmatched ones
        for i in range(min_len, len(distribution_data)):
            distribution_data[i]["customer_type"] = ""
            distribution_data[i]["percentage"] = 0

        # Build and return the response
        return self._build_response(yearly_projections, distribution_data)

    def _build_response(self, projections, distribution_data):
        """Build the final response."""
        growth_serializer = GrowthProjectionSerializer(data=projections, many=True)
        distribution_serializer = CustomerTypeDistributionSerializer(data=distribution_data, many=True)

        if growth_serializer.is_valid() and (not distribution_data or distribution_serializer.is_valid()):
            return Response(
                {
                    "success": True,
                    "data": {
                        "growth_projection": growth_serializer.validated_data,
                        "customer_distribution": distribution_serializer.validated_data if distribution_data else [],
                    },
                },
                status=status.HTTP_200_OK,
            )

        errors = {
            "growth_projection": growth_serializer.errors if not growth_serializer.is_valid() else None,
            "customer_distribution": distribution_serializer.errors if distribution_data and not distribution_serializer.is_valid() else None,
        }
        return self._error_response(errors, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _error_response(self, error, status_code):
        """Helper to return error responses."""
        return Response({"success": False, "error": error}, status=status_code)