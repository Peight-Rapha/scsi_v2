from django.contrib import admin

from base.models import TenantAdminMixin

from .models import Agent, Commission, Producer


@admin.register(Agent)
class AgentAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'type', 'commission_rate', 'brokerage')
    list_filter = ('brokerage', 'type', 'created_at')
    search_fields = ('name', 'document')


@admin.register(Producer)
class ProducerAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'agent', 'commission_rate', 'brokerage')
    list_filter = ('brokerage', 'created_at')
    search_fields = ('name', 'document', 'agent__name')


@admin.register(Commission)
class CommissionAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('policy', 'gross_amount', 'brokerage_amount', 'agent_amount', 'producer_amount', 'status', 'brokerage')
    list_filter = ('brokerage', 'status', 'created_at')
    search_fields = ('policy__policy_number', 'agent__name', 'producer__name')
