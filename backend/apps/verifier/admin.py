from django.contrib import admin
from django.contrib import admin
from .models import EmailVerificationLog, UserPlan, Plan

# Register Logs Model
@admin.register(EmailVerificationLog)
class EmailVerificationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'deliverable', 'timestamp')
    list_filter = ('deliverable', 'is_disposable', 'timestamp')
    search_fields = ('email', 'user__username')

# User Credits Model
admin.site.register(UserPlan)

admin.site.register(Plan)