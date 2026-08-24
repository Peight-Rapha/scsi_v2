from django.contrib import admin

from base.models import TenantAdminMixin

from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('original_name', 'uploaded_by', 'client', 'proposal', 'policy', 'claim', 'size_bytes', 'brokerage')
    list_filter = ('brokerage', 'created_at', 'content_type')
    search_fields = ('original_name', 'uploaded_by__email')
