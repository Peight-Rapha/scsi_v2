from django.contrib import admin

from base.models import TenantAdminMixin

from .models import Claim


@admin.register(Claim)
class ClaimAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('claim_number', 'client', 'policy', 'covered_item', 'status', 'occurred_at', 'brokerage')
    list_filter = ('status', 'brokerage', 'policy__insurance_company', 'occurred_at', 'created_at')
    search_fields = ('claim_number', 'client__name', 'policy__policy_number')
