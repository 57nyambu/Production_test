from django.contrib import admin
from .models import (
    CompanyInformation, WorkingCapital, RevenueStream, RevenueDrivers,
    CostStracture, EmployeeInfo, AdminMarketingExp, AllExpenses,
    Asset, Capex, DividendPolicy, IndustryMetrics,HistoricalFinData, 

)

admin.site.register(Capex)

