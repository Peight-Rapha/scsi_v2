from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.models import BrokerageScopedFormKwargsMixin, TenantObjectMixin, TenantQuerySetMixin
from base.views import InternalViewMixin

from .forms import ClaimForm
from .models import Claim


class ClaimListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Claim
    template_name = 'claims/claim_list.html'
    context_object_name = 'claims'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('client', 'policy', 'policy__insurance_company', 'covered_item')
        status = self.request.GET.get('status')
        policy = self.request.GET.get('policy')
        insurer = self.request.GET.get('insurer')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(Q(claim_number__icontains=search) | Q(client__name__icontains=search))
        if status:
            queryset = queryset.filter(status=status)
        if policy:
            queryset = queryset.filter(policy_id=policy)
        if insurer:
            queryset = queryset.filter(policy__insurance_company_id=insurer)
        if start:
            queryset = queryset.filter(occurred_at__gte=start)
        if end:
            queryset = queryset.filter(occurred_at__lte=end)
        return queryset


class ClaimDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = Claim
    template_name = 'claims/claim_detail.html'


class ClaimCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, CreateView):
    model = Claim
    form_class = ClaimForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Novo sinistro'}


class ClaimUpdateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, UpdateView):
    model = Claim
    form_class = ClaimForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar sinistro'}


class ClaimDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = Claim
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('claims:list')
