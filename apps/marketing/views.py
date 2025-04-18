from .models import MarketingMetrics
from .serializers import (
    MarketingMetricsSerializer,
    GrowthProjectionSerializer,
    CustomerTypeDistributionSerializer,
)
from apps.utils.baseViews import BaseAPIView, BaseReadOnlyView
from rest_framework.response import Response
from rest_framework import status
from apps.customer.models import CustomerDistribution


class MarketingMetricsView(BaseAPIView):
    """View to handle Marketing Metrics API requests."""
    model = MarketingMetrics
    serializer_class = MarketingMetricsSerializer


class GrowthProjectionView(BaseReadOnlyView):
    """View to handle Growth Projection API requests."""
    model_class = MarketingMetrics
    serializer_class = MarketingMetricsSerializer

    def get(self, request, *args, **kwargs):
        """Handle GET request for growth projection."""
        instance = self.model_class.objects.filter(user=request.user).first()
        if not instance:
            return self._error_response(f"No data found for {self.model_class.__name__}.", status.HTTP_404_NOT_FOUND)

        growth_rates = sorted(instance.growth_rate.all(), key=lambda x: x.year)
        if not growth_rates:
            return self._error_response("No growth rates found for projection.", status.HTTP_400_BAD_REQUEST)

        yearly_projections = self._calculate_growth_projections(instance.new_monthly_customers, growth_rates)
        distribution_data = self._calculate_customer_distribution(request.user, yearly_projections)

        return self._build_response(yearly_projections, distribution_data)

    def _calculate_growth_projections(self, initial_customers, growth_rates):
        """Calculate yearly growth projections."""
        total_customers = initial_customers
        projections = []
        for growth in growth_rates:
            projections.append({"year": growth.year, "customers": int(total_customers)})
            total_customers *= (1 + float(growth.rate) / 100)
        return projections

    def _calculate_customer_distribution(self, user, yearly_projections):
        """Calculate customer distribution based on the first year's total."""
        first_year_total = yearly_projections[0]["customers"] if yearly_projections else 0
        customer_distributions = CustomerDistribution.objects.filter(user=user)
        return [
            {
                "customer_type": dist.customer_type,
                "count": int(first_year_total * float(dist.percentage) / 100),
                "percentage": float(dist.percentage),
            }
            for dist in customer_distributions
        ]

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