from .models import CustomerModel, CustomerDistribution, ChurnRate
from apps.marketing.models import MarketingMetrics, GrowthRate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (
    CustomerModelSerializer,
    OrganicCustomerChurnRateSerializer,
    OrganicCustomerGrowthProjectionSerializer,
    OrganicCustDistributionSerializer
)
from apps.utils.baseViews import BaseAPIView, BaseReadOnlyView

class CustomerModelView(BaseAPIView):
    model = CustomerModel
    serializer_class = CustomerModelSerializer


class OrganicCustomerMetricsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        # Get the CustomerModel for the logged-in user
        customer_model = CustomerModel.objects.filter(user=request.user).first()
        if not customer_model:
            return Response({"success": False, "message": "No customer data found."})

        # Get the beginning client count
        beginning_client = customer_model.beginning_client

        # Filter for organic customers
        organic_distribution = customer_model.cust_distribution.filter(customer_type='organic').first()
        if not organic_distribution:
            return Response({"success": False, "message": "No organic customer data found."})

        organic_percentage = organic_distribution.percentage / 100  # Convert to decimal

        # Calculate initial organic customers
        organic_clients = int(beginning_client * organic_percentage)

        # Calculate growth for the logged-in user
        growth_rates = GrowthRate.objects.filter(user=request.user).order_by('year')
        organic_cust_growth = []
        current_customers = organic_clients
        for growth in growth_rates:
            growth_customers = int(current_customers * (1 + growth.rate / 100))
            organic_cust_growth.append({
                "year": growth.year,
                "customers": growth_customers
            })
            current_customers = growth_customers  # Update for the next year's growth

        # Calculate churn for the logged-in user
        churn_rates = ChurnRate.objects.filter(user=request.user).order_by('year')
        organic_cust_churn = []
        current_customers = organic_clients
        for churn in churn_rates:
            remaining_customers = int(current_customers * (1 - churn.rate / 100))
            organic_cust_churn.append({
                "year": churn.year,
                "customers": remaining_customers
            })
            current_customers = remaining_customers  # Update for the next year's churn

        # Response data
        data = {
            "beginning_client": beginning_client,  # Add beginning_client to the response
            "organic_cust_growth": organic_cust_growth,
            "organic_cust_churn": organic_cust_churn
        }
        return Response({"success": True, "data": data})