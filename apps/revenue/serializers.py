from rest_framework import serializers
from .models import RevenueModel
from apps.utils.baseSerializers import BaseCombinedSerializer


class RevenueModelSerializer(BaseCombinedSerializer):
    class Meta(BaseCombinedSerializer.Meta):
        model = RevenueModel
        fields = BaseCombinedSerializer.Meta.fields + [
            "percentage_comm", "units_sold"]