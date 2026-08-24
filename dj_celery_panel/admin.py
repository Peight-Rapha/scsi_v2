from django.contrib import admin

from .models import CeleryTaskEvent


@admin.register(CeleryTaskEvent)
class CeleryTaskEventAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'task_id', 'status', 'brokerage_id', 'user_id', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('task_name', 'task_id', 'message')
    readonly_fields = ('created_at', 'updated_at')
