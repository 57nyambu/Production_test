from apps.financials.models import (
    CompanyInformation, WorkingCapital, RevenueStream, RevenueDrivers,
    CostStracture, EmployeeInfo, AdminMarketingExp, AllExpenses,
    Asset, Capex, DividendPolicy, IndustryMetrics,HistoricalFinData, 
)
from apps.marketing.models import MarketingMetrics
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal


class OutputCalculations:
    def _error_response(self, error, status_code):
        """Helper to return error responses."""
        return Response({"success": False, "error": error}, status=status_code)

    def cogs_calculations(self, request, *args, **kwargs):
        revenue_instance = RevenueDrivers.objects.filter(user=request.user).first()
        if not revenue_instance:
            return self._error_response("No data found!", status.HTTP_404_NOT_FOUND)
        
        cogs_instance = CostStracture.objects.filter(user=request.user).first()
        if not cogs_instance:
            return self._error_response("No data found!", status.HTTP_404_NOT_FOUND)
        
        total_revenue = revenue_instance.calculate_revenue()
        total_cogs = cogs_instance.cogs_calculation()

        self.gross_profit = total_revenue - total_cogs
        gross_mirgin = round((self.gross_profit / total_revenue) * 100, 2)  # Round to 2 decimal places

        return {
            "revenue": total_revenue,
            "cogs": total_cogs,
            "gross_profit": self.gross_profit,
            "gross_mirgin": Decimal(gross_mirgin)  # Ensure it's a Decimal for the serializer
        }
    
    def expenses_calc(self, request, *args, **kwargs):
        sales_exp = 0
        market_instance = MarketingMetrics.objects.filter(user=request.user).first()
        if not market_instance:
            return self._error_response("No data found!", status.HTTP_404_NOT_FOUND)
        
        marketing_exp = market_instance.yearly_marketing_cost
        research_dev = 0
        expens_instance = AllExpenses.objects.filter(user=request.user).first()
        if not expens_instance:
            return self._error_response("No data found!", status.HTTP_404_NOT_FOUND)

        all_expens = expens_instance.all_expens_calc()
        self.total_exp = (sales_exp + all_expens)

        return {
            "sales_exp": sales_exp,
            "marketing_exp": marketing_exp,
            "research_dev": research_dev,
            "gen_admin": all_expens,
            "total_exp": self.total_exp
        }
    
    def operating_ebitda_income(self):
        operating_income = self.gross_profit - self.total_exp
        depriciation = 0
        armotization = 0
        self.ebit = operating_income - (depriciation + armotization)

        return {
            "operating_income": operating_income,
            "depriciation": depriciation,
            "armotization": armotization,
            "ebit": self.ebit
        }
    
    def net_income_calc(self):
        interest_exp = 0
        pretax_income = self.ebit - interest_exp
        tax = 0
        net_income = pretax_income - tax

        return {
            "interest_exp": interest_exp,
            "pretax_income": pretax_income,
            "tax": tax,
            "net_income": net_income
        }