from django.contrib import admin
from .models import (
    CompanyInformation, WorkingCapital, RevenueStream, RevenueDrivers,
    CostStracture, EmployeeInfo, AdminMarketingExp, AllExpenses,
    Asset, Capex, DividendPolicy, IndustryMetrics,HistoricalFinData, 

)
admin.site.register(CompanyInformation)
admin.site.register(WorkingCapital)
admin.site.register(RevenueStream)
admin.site.register(RevenueDrivers)
admin.site.register(CostStracture)
admin.site.register(EmployeeInfo)
admin.site.register(AdminMarketingExp)
admin.site.register(AllExpenses)
admin.site.register(Asset)
admin.site.register(Capex)
admin.site.register(DividendPolicy)
admin.site.register(IndustryMetrics)
admin.site.register(HistoricalFinData)

