from django.contrib import admin

from base.models import TenantAdminMixin

from .models import AIChatMessage, AIChatSession


@admin.register(AIChatSession)
class AIChatSessionAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'user', 'brokerage', 'updated_at')
    list_filter = ('brokerage', 'created_at', 'updated_at')
    search_fields = ('title', 'user__email')


@admin.register(AIChatMessage)
class AIChatMessageAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('session', 'role', 'brokerage', 'created_at')
    list_filter = ('brokerage', 'role', 'created_at')
    search_fields = ('content_markdown', 'session__title')
