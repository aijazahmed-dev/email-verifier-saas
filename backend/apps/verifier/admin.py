from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EmailVerificationLog

@admin.register(EmailVerificationLog)
class EmailVerificationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'deliverable', 'timestamp')
    list_filter = ('deliverable', 'is_disposable', 'timestamp')
    search_fields = ('email', 'user__username')
