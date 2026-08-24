from django.contrib import admin

from base.models import TenantAdminMixin

from .models import Client


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'document', 'email', 'phone', 'type', 'brokerage')
    list_filter = ('type', 'brokerage', 'created_at')
    search_fields = ('name', 'document', 'email', 'phone')
