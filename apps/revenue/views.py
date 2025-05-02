from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import RevenueModel
from .serializers import RevenueModelSerializer
from apps.utils.baseViews import BaseAPIView
from apps.customer.models import CustomerModel, CustomerDistribution
from apps.financials.models import RevenueDrivers
from apps.marketing.models import GrowthRate

class RevenueView(BaseAPIView):
    model = RevenueModel
    serializer_class = RevenueModelSerializer


class RevenueOutputView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get customer distribution for the logged-in user
        customer_distributions = CustomerDistribution.objects.filter(user=request.user)
        if not customer_distributions.exists():
            return self._error_response("No customer distribution data found.", status.HTTP_404_NOT_FOUND)

        # Get growth rates for the logged-in user
        growth_rates = GrowthRate.objects.filter(user=request.user).order_by('year')
        if not growth_rates.exists():
            return self._error_response("No growth rate data found.", status.HTTP_404_NOT_FOUND)

        # Get total revenue for the logged-in user
        revenue_instance = RevenueDrivers.objects.filter(user=request.user).first()
        if not revenue_instance:
            return self._error_response("No revenue data found.", status.HTTP_404_NOT_FOUND)
        total_revenue = Decimal(revenue_instance.calculate_revenue())  # Ensure total_revenue is a Decimal

        # Get beginning customers from the marketing model
        customer_model = CustomerModel.objects.filter(user=request.user).first()
        if not customer_model:
            return self._error_response("No customer data found.", status.HTTP_404_NOT_FOUND)
        beginning_customers = customer_model.beginning_client

        # Initialize yearly data
        yearly_data = {}
        current_customers = beginning_customers

        # Iterate through growth rates to calculate yearly data
        for growth in growth_rates:
            year = growth.year
            growth_rate = Decimal(growth.rate) / Decimal(100)  # Use Decimal for growth rate

            # Calculate the total number of customers for the year
            current_customers = int(current_customers * (1 + growth_rate))  # Use customer growth rate
            yearly_data[year] = []

            # Calculate customer distribution for the year
            for dist in customer_distributions:
                customer_percentage = Decimal(dist.percentage) / Decimal(100)  # Use Decimal for percentage
                customer_count = int(current_customers * customer_percentage)  # Correct customer count
                customer_amount = total_revenue * customer_percentage  # Adjusted revenue amount

                yearly_data[year].append({
                    "cust_type": dist.customer_type,
                    "amount": round(customer_amount, 2),  # Round to 2 decimal places
                    "count": customer_count
                })

        # Return the calculated yearly data
        return Response({"success": True, "data": yearly_data})

    def _error_response(self, error, status_code):
        return Response({
            "success": False,
            "error": error
        }, status=status_code)