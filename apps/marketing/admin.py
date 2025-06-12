from django.contrib import admin
from .models import MarketingMetrics, MarketingComponent, GrowthRate

admin.site.register(MarketingMetrics)
admin.site.register(MarketingComponent)
admin.site.register(GrowthRate)

# Register your models here.
