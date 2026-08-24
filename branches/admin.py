from django.contrib import admin

from base.models import TenantAdminMixin

from .models import InsuranceBranch


@admin.register(InsuranceBranch)
class InsuranceBranchAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'brokerage', 'created_at')
    list_filter = ('brokerage', 'created_at')
    search_fields = ('name', 'description')
