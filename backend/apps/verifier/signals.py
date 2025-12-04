from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserCredits

@receiver(post_save, sender=User)
def create_user_credits(sender, instance, created, **kwargs):
    """
    Signal to automatically create a UserCredits record when a new user is registered.

    :param sender: The model class that sent the signal (User model).
    :param instance: The actual instance of the User that was just saved.
    :param created: Boolean value; True if a new User was created, False if an existing User was updated.
    :param **kwargs: Additional keyword arguments (not used here).
    """
    if created:
        UserCredits.objects.create(user=instance)