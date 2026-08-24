from django.contrib import admin

from base.models import TenantAdminMixin

from .models import CoveredItem


@admin.register(CoveredItem)
class CoveredItemAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('description', 'item_type', 'insured_value', 'proposal', 'policy_id', 'brokerage')
    list_filter = ('item_type', 'brokerage', 'created_at')
    search_fields = ('description', 'proposal__client__name')
