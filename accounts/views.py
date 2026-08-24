from django.contrib.auth import get_user_model
from django.views.generic import ListView

from base.views import InternalViewMixin


class UserListView(InternalViewMixin, ListView):
    model = get_user_model()
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('email')
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(brokerage=self.request.brokerage)
