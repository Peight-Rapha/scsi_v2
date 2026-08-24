from django.contrib import admin

from base.models import TenantAdminMixin

from .models import Policy


@admin.register(Policy)
class PolicyAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('policy_number', 'client', 'insurance_company', 'branch', 'status', 'end_date', 'brokerage')
    list_filter = ('status', 'brokerage', 'end_date', 'created_at')
    search_fields = ('policy_number', 'client__name', 'insurance_company__name')
