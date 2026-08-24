from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView

from base.models import TenantQuerySetMixin, get_tenant_object_or_404
from base.views import InternalViewMixin

from .models import Notification


class NotificationListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Notification
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class NotificationReadView(InternalViewMixin, View):
    def post(self, request, pk):
        notification = get_tenant_object_or_404(Notification, request.brokerage, pk=pk, user=request.user)
        notification.is_read = True
        notification.save(update_fields=['is_read', 'updated_at'])
        return redirect('notifications:list')
