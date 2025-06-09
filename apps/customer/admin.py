from django.contrib import admin
from .models import CustomerModel, CustomerDistribution, ChurnRate

admin.site.register(CustomerModel)
admin.site.register(CustomerDistribution)
admin.site.register(ChurnRate)

# Register your models here.
