from django.contrib import admin

from base.models import TenantAdminMixin

from .models import Renewal


@admin.register(Renewal)
class RenewalAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('policy', 'due_date', 'status', 'is_due_soon', 'brokerage')
    list_filter = ('status', 'due_date', 'brokerage')
    search_fields = ('policy__policy_number', 'policy__client__name')
