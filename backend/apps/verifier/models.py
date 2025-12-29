from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Logs and history model
class EmailVerificationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    syntax_valid = models.BooleanField()
    has_mx = models.BooleanField()
    is_disposable = models.BooleanField()
    is_role = models.BooleanField()
    deliverable = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} by {self.user.username} at {self.timestamp}"
    
# User Plans Models
class Plan(models.Model):
    name = models.CharField(max_length=50)  
    price = models.IntegerField(default=0)  # PKR
    credits = models.IntegerField(default=0)
    is_monthly = models.BooleanField(default=False)  # Free plan = True
    daily_limit = models.IntegerField(default=0)  # Free plan = 20, others = 0 (no limit)
    monthly_limit = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    credits_remaining = models.IntegerField(default=0)
    daily_used = models.IntegerField(default=0)
    monthly_used = models.IntegerField(default=0)
    last_daily_reset = models.DateField(default=timezone.now)
    last_monthly_reset = models.DateField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old = UserPlan.objects.get(pk=self.pk)
            if old.plan != self.plan:
                self.credits_remaining = self.plan.credits
        else:
            if self.plan:
                self.credits_remaining = self.plan.credits

        super().save(*args, **kwargs)