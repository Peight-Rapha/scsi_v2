from datetime import timedelta

from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.models import BrokerageScopedFormKwargsMixin, TenantObjectMixin, TenantQuerySetMixin
from base.views import InternalViewMixin

from .forms import RenewalForm
from .models import Renewal


class RenewalListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Renewal
    template_name = 'renewals/renewal_list.html'
    context_object_name = 'renewals'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('policy', 'policy__client')
        status = self.request.GET.get('status')
        days = self.request.GET.get('days')
        if status:
            queryset = queryset.filter(status=status)
        if days:
            queryset = queryset.filter(due_date__lte=timezone.localdate() + timedelta(days=int(days)))
        return queryset


class RenewalDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = Renewal
    template_name = 'generic/detail.html'


class RenewalCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, CreateView):
    model = Renewal
    form_class = RenewalForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Nova renovação'}


class RenewalUpdateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, UpdateView):
    model = Renewal
    form_class = RenewalForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar renovação'}


class RenewalDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = Renewal
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('renewals:list')
