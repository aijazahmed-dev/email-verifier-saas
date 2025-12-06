from django.utils import timezone

# Daily & Monthly Reset Logic (Auto-Reset)
def reset_user_credits(user_plan):
    today = timezone.now().date()

    # Reset daily usage
    if user_plan.last_daily_reset != today:
        user_plan.daily_used = 0
        user_plan.last_daily_reset = today

    # Reset monthly usage (Free plan only)
    if user_plan.plan.is_monthly:
        if user_plan.last_monthly_reset.month != today.month:
            user_plan.credits_remaining = user_plan.plan.credits   # Reset to default monthly credits
            user_plan.last_monthly_reset = today

    user_plan.save()
