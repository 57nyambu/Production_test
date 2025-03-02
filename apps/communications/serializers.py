from rest_framework import serializers
from .models import Emails
from apps.subscriptions.models import Subscription
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']
        
        # Check if the user is registered
        user = User.objects.filter(email=email).first()
        is_registered = bool(user)

        # Default to False if user not found
        is_subscribed = False  

        if user:
            # Check if the user has a subscription
            subscription = Subscription.objects.filter(user=user, is_active=True).first()
            if subscription and subscription.plan and subscription.plan.id != 1:
                is_subscribed = True  # Not using Free Plan

        # Save or update email entry
        email_obj, created = Emails.objects.update_or_create(
            email=email,
            defaults={
                "is_registered": is_registered,
                "is_subscribed": is_subscribed,
            }
        )
        
        return email_obj
    

class EmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = '__all__'  # Returns all fields in the model
