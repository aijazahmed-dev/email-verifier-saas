from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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