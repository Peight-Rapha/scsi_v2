from django.contrib import admin

from .models import Brokerage


@admin.register(Brokerage)
class BrokerageAdmin(admin.ModelAdmin):
    list_display = ('name', 'legal_name', 'cnpj', 'plan', 'is_active')
    list_filter = ('plan', 'is_active')
    search_fields = ('name', 'legal_name', 'cnpj')
