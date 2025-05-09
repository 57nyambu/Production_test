from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import OutputCalculations
from .serializers import (
    CombinedOutputSerializer
)
from rest_framework.permissions import IsAuthenticated

class IncomeOutputView(APIView):
    """For view-only operations"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Call the service for calculations
        service = OutputCalculations()

        # Collect data from all calculation methods
        cogs_data = service.cogs_calculations(request)
        if isinstance(cogs_data, Response):  # Check for error response
            return cogs_data

        expenses_data = service.expenses_calc(request)
        if isinstance(expenses_data, Response):  # Check for error response
            return expenses_data

        operations_data = service.operating_ebitda_income()
        net_income_data = service.net_income_calc()

        # Combine all data into a single dictionary
        combined_data = {
            "revenue": cogs_data,
            "expenses": expenses_data,
            "operations": operations_data,
            "netincome": net_income_data
        }

        # Serialize the combined data
        serializer = CombinedOutputSerializer(data=combined_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)