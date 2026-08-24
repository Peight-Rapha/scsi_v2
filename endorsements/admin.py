from django.contrib import admin

from base.models import TenantAdminMixin

from .models import Endorsement


@admin.register(Endorsement)
class EndorsementAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('endorsement_number', 'policy', 'type', 'effective_date', 'brokerage')
    list_filter = ('brokerage', 'type', 'effective_date', 'created_at')
    search_fields = ('endorsement_number', 'description', 'policy__policy_number')
