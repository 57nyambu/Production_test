from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import CustomUser

from apps.subscriptions.models import Plan, Subscription

@receiver(post_save, sender=CustomUser)
def create_user_subscription(sender, instance, created, **kwargs):
    if created:
        default_plan = Plan.objects.get_or_create(
            name='Free',
            defaults={'price': 0, 'features': {'api_calls': 100}}
        )[0]
        Subscription.objects.create(user=instance, plan=default_plan)
