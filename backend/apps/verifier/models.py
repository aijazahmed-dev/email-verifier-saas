from django.db import models
from django.contrib.auth.models import User

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
    
# User Credits Models
class UserCredits(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.user.username} - {self.credits} Credits"