from django.contrib import admin

from base.models import TenantAdminMixin

from .models import Deal, DealStage


@admin.register(DealStage)
class DealStageAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'color', 'position', 'brokerage')
    list_filter = ('brokerage',)
    search_fields = ('name',)


@admin.register(Deal)
class DealAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'client', 'stage', 'estimated_value', 'status', 'assigned_to', 'brokerage')
    list_filter = ('status', 'stage', 'brokerage', 'assigned_to')
    search_fields = ('title', 'client__name', 'assigned_to__email')
