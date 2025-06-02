from django.apps import AppConfig


class FinancialsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.financials'

"""
from apps.financials.models import RevenueDrivers
for driver in RevenueDrivers.objects.all():
    for stream in driver.revenue_streams.all():
        stream.driver = driver
        stream.save()
Then this
from apps.financials.models import RevenueDrivers, RevenueStream
for s in RevenueStream.objects.all():
    print(f"{s.name} => {s.driver.units_sold if s.driver else 'No driver'}")"""
