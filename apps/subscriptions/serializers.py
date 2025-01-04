from rest_framework import serializers
from .models import Plan, Subscription

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'features', 'period']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'plan_id', 'start_date', 'end_date', 'is_active']
        read_only_fields = ['start_date', 'is_active']