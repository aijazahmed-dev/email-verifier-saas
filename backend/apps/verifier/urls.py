from django.urls import path
from .views import emails_check

urlpatterns = [
    path("emails-check/", emails_check, name="emails_check"),
]