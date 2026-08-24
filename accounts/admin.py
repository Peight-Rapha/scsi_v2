from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'brokerage', 'is_staff', 'is_active')
    list_filter = ('brokerage', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Dados pessoais', {'fields': ('first_name', 'last_name', 'brokerage')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'brokerage', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(brokerage=getattr(request.user, 'brokerage', None))
