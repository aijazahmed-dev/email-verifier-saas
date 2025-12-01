from django.urls import path
from .views import emails_check, bulk_csv_check_view, download_bulk_results

urlpatterns = [
    path("emails-check/", emails_check, name="emails_check"),
    path('bulk-emails/', bulk_csv_check_view, name='bulk_csv_check'),
    path('bulk-emails/download/', download_bulk_results, name='download_bulk_results'),
]