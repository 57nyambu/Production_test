from django.apps import AppConfig


class CombmodelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.marketing'

"""
from apps.marketing.models import MarketingMetrics
for driver in MarketingMetrics.objects.all():
    for stream in driver.revenue_streams.all():
        stream.driver = driver
        stream.save()
Then this
from apps.marketing.models import MarketingMetrics, GrowthRate
for s in GrowthRate.objects.all():
    print(f"{s.year} => {s.driver.units_sold if s.driver else 'No driver'}")"""
