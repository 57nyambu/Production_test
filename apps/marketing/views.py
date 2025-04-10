from .models import MarketingMetrics
from .serializers import MarketingMetricsSerializer, GrowthProjectionSerializer, CustomerTypeDistributionSerializer
from apps.utils.baseViews import BaseAPIView, BaseReadOnlyView
from rest_framework.views import APIView
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
        try:
            # Get the marketing metrics instance for the current user
            instance = self.model_class.objects.filter(user=request.user).first()

            if not instance:
                return Response(
                    {"success": False, "error": f"No data found for {self.model_class.__name__}."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Extract and sort growth rates by year
            growth_rates = sorted(instance.growth_rate.all(), key=lambda x: x.year)
            
            if not growth_rates:
                return Response(
                    {"success": False, "error": "No growth rates found for projection."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Initialize first year customers from instance
            total_customers = instance.new_monthly_customers
            yearly_projections = []

            # Compute customer growth for each provided year
            for growth in growth_rates:
                yearly_projections.append({
                    "year": growth.year,
                    "customers": int(total_customers)
                })
                # Apply growth rate for next year
                total_customers *= (1 + float(growth.rate) / 100)

            # Get customer distribution data
            # Assuming there's a relationship to CustomerDistribution in your models
            # If not, you'll need to adjust this query accordingly
            customer_distributions = CustomerDistribution.objects.filter(user=request.user)
            
            # Calculate customer counts by type
            distribution_data = []
            # Use the total from the first year projection for distribution calculation
            first_year_total = yearly_projections[0]["customers"] if yearly_projections else 0
            
            for dist in customer_distributions:
                # Calculate the actual count based on percentage
                customer_count = int(first_year_total * float(dist.percentage) / 100)
                
                # Create the distribution entry with explicitly set fields
                distribution_entry = {
                    "customer_type": dist.customer_type,
                    "count": customer_count,  # Ensure this field is included
                    "percentage": float(dist.percentage)
                }
                distribution_data.append(distribution_entry)

            # Validate output data
            growth_serializer = GrowthProjectionSerializer(data=yearly_projections, many=True)
            
            # Make sure we actually have distribution data before trying to validate it
            if not distribution_data:
                # If no distribution data is found, just include growth projection
                if growth_serializer.is_valid():
                    return Response(
                        {
                            "success": True, 
                            "data": {
                                "growth_projection": growth_serializer.validated_data
                            }
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"success": False, "error": growth_serializer.errors},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            
            # If we have distribution data, validate and include it
            distribution_serializer = CustomerTypeDistributionSerializer(data=distribution_data, many=True)
            
            if growth_serializer.is_valid() and distribution_serializer.is_valid():
                # Structure response with both data sections
                return Response(
                    {
                        "success": True, 
                        "data": {
                            "growth_projection": growth_serializer.validated_data,
                            "customer_distribution": distribution_serializer.validated_data
                        }
                    },
                    status=status.HTTP_200_OK
                )
            else:
                errors = {}
                if not growth_serializer.is_valid():
                    errors["growth_projection"] = growth_serializer.errors
                if not distribution_serializer.is_valid():
                    errors["customer_distribution"] = distribution_serializer.errors
                
                return Response(
                    {"success": False, "error": errors},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            import traceback
            return Response(
                {"success": False, "error": str(e), "traceback": traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )