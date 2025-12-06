# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserPlan, Plan

@receiver(post_save, sender=User)
def create_user_plan(sender, instance, created, **kwargs):
    if created:
        free_plan = Plan.objects.get(name="Free")
        UserPlan.objects.create(
            user=instance,
            plan=free_plan,
            credits_remaining=free_plan.credits
        )
