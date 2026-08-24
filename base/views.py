from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CurrentBrokerageRequiredMixin


class InternalViewMixin(LoginRequiredMixin, CurrentBrokerageRequiredMixin):
    pass
