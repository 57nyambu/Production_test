from django.apps import AppConfig

class CustRevConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.customer'

"""
from apps.customer.models import CustomerModel, CustomerDistribution
for c_model in CustomerModel.objects.all():
    for type in c_model.cust_type.all():
        type.c_model = c_model
        type.save()
Then this
from apps.customer.models import CustomerModel, CustomerDistribution
for s in CustomerDistribution.objects.all():
    print(f"{s.customer_type} => {s.cust_model.organic_client if s.cust_model else 'No Model'}")

    
from apps.customer.models import CustomerDistribution
for m in CustomerDistribution.objects.all():
    print(f"{s.cust_model.organic_client if s.cust_model else 'No Model'}")
"""
