from django.contrib import admin

from base.models import TenantAdminMixin

from .models import InsuranceCompany


@admin.register(InsuranceCompany)
class InsuranceCompanyAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'contact_email', 'contact_phone', 'brokerage')
    list_filter = ('brokerage', 'created_at')
    search_fields = ('name', 'cnpj', 'contact_email')
