from django.utils import timezone
from datetime import timedelta
from .models import UserPlan

# Daily & Monthly Reset Logic (Auto-Reset)
def reset_user_credits(user_plan):
    today = timezone.now().date()

    # Reset daily usage
    if user_plan.plan.daily_limit > 0:
        if user_plan.last_daily_reset != today:
            user_plan.daily_used = 0
            user_plan.last_daily_reset = today

    # Reset monthly usage for all plans with monthly_limit
    if user_plan.plan.monthly_limit > 0:
        if (user_plan.last_monthly_reset.month != today.month or 
            user_plan.last_monthly_reset.year != today.year):
            user_plan.monthly_used = 0
            user_plan.last_monthly_reset = today

    # Reset monthly usage (Free plan only)
    if user_plan.plan.is_monthly:
        if user_plan.last_monthly_reset.month != today.month:
            user_plan.credits_remaining = user_plan.plan.credits
            user_plan.last_monthly_reset = today

    user_plan.save()

# Purchase Plans
def purchase_plan(user, plan):
    user_plan = UserPlan.objects.get(user=user)
    user_plan.plan = plan
    user_plan.credits_remaining = plan.credits
    user_plan.daily_used = 0

    # Set expiry date only for monthly-paid plans
    if plan.name in ["Basic", "Pro"]:
        user_plan.expiry_date = timezone.now().date() + timedelta(days=30)
    else:
        user_plan.expiry_date = None  # Free/Premium

    user_plan.save()

