from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.models import BrokerageScopedFormKwargsMixin, TenantObjectMixin, TenantQuerySetMixin, get_tenant_object_or_404
from base.views import InternalViewMixin
from proposals.models import Proposal

from .forms import PolicyForm
from .models import Policy
from .services import generate_policy_from_proposal


class PolicyListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Policy
    template_name = 'generic/object_list.html'
    context_object_name = 'objects'
    extra_context = {'title': 'Apólices', 'create_url_name': 'policies:create'}

    def get_queryset(self):
        queryset = super().get_queryset().select_related('client', 'insurance_company', 'branch', 'proposal')
        search = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if search:
            queryset = queryset.filter(Q(policy_number__icontains=search) | Q(client__name__icontains=search))
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class PolicyDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = Policy
    template_name = 'policies/policy_detail.html'


class PolicyCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, CreateView):
    model = Policy
    form_class = PolicyForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Nova apólice'}


class PolicyUpdateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, UpdateView):
    model = Policy
    form_class = PolicyForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar apólice'}


class PolicyDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = Policy
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('policies:list')


class GeneratePolicyView(InternalViewMixin, View):
    def post(self, request, proposal_pk):
        proposal = get_tenant_object_or_404(Proposal, request.brokerage, pk=proposal_pk)
        policy = generate_policy_from_proposal(proposal)
        return redirect(policy.get_absolute_url())
