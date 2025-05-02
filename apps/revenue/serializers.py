from rest_framework import serializers
from .models import RevenueModel
from apps.utils.baseSerializers import BaseCombinedSerializer
from apps.financials.models import RevenueStream
from apps.customer.models import CustomerDistribution



class RevenueModelSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = RevenueModel
        fields = BaseCombinedSerializer.Meta.fields + [
            "percentage_comm", "units_sold"]
        

class RevenueOutputSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    cust_type = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    count = serializers.IntegerField()