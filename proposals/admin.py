from django.contrib import admin

from base.models import TenantAdminMixin

from .models import Coverage, Proposal


@admin.register(Proposal)
class ProposalAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'client', 'insurance_company', 'branch', 'status', 'premium_amount', 'brokerage')
    list_filter = ('status', 'brokerage', 'created_at', 'valid_until')
    search_fields = ('client__name', 'insurance_company__name', 'branch__name')


@admin.register(Coverage)
class CoverageAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'proposal', 'policy_id', 'limit_amount', 'deductible_amount', 'brokerage')
    list_filter = ('brokerage', 'created_at')
    search_fields = ('name', 'proposal__client__name')
