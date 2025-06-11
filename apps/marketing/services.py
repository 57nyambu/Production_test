from rest_framework import status
from .models import MarketingMetrics
from apps.customer.models import CustomerDistribution, CustomerModel
from apps.financials.models import RevenueStream
from typing import Tuple, Dict, Any, Optional

def get_growth_metrics(user) -> Tuple[Optional[Dict[str, Any]], Optional[str], int]:
    """
    Get growth projection and customer distribution metrics.
    Returns: (data, error_message, status_code)
    """
    # Get MarketingMetrics
    instance = MarketingMetrics.objects.filter(user=user).first()
    if not instance:
        return None, "No data found for MarketingMetrics.", status.HTTP_404_NOT_FOUND

    # Get CustomerModel
    customer_instance = CustomerModel.objects.filter(user=user).first()
    if not customer_instance:
        return None, "No data found for CustomerModel.", status.HTTP_404_NOT_FOUND

    try:
        # Get growth projections
        yearly_projections = instance.calculate_growth_projections(
            customer_instance.beginning_client
        )
        if not yearly_projections:
            return None, "No growth rates found for projection.", status.HTTP_400_BAD_REQUEST

        # Get customer distribution
        distribution_data = get_customer_distribution(
            user, 
            yearly_projections[0]["customers"]
        )

        return {
            "growth_projection": yearly_projections,
            "customer_distribution": distribution_data
        }, None, status.HTTP_200_OK

    except Exception as e:
        return None, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR

def get_customer_distribution(user, total_customers: int) -> list:
    """
    Get customer distribution data with revenue stream information.
    """
    # Get base distribution
    distribution_data = CustomerDistribution.calculate_distribution(
        user, 
        total_customers
    )

    # Get revenue streams
    revenue_streams = RevenueStream.objects.filter(user=user)
    
    # Update distribution with revenue stream data
    for dist, stream in zip(distribution_data, revenue_streams):
        dist["customer_type"] = stream.name
        dist["percentage"] = stream.percentage

    return distribution_data