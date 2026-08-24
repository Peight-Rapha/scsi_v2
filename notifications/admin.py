from django.contrib import admin

from base.models import TenantAdminMixin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'user', 'level', 'is_read', 'brokerage', 'created_at')
    list_filter = ('brokerage', 'level', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__email')
