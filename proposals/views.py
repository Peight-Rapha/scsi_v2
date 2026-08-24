from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.models import BrokerageScopedFormKwargsMixin, TenantObjectMixin, TenantQuerySetMixin, get_tenant_object_or_404
from base.views import InternalViewMixin
from covered_items.forms import CoveredItemForm

from .forms import CoverageForm, ProposalForm
from .models import Coverage, Proposal


class ProposalListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Proposal
    template_name = 'proposals/proposal_list.html'
    context_object_name = 'proposals'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('client', 'insurance_company', 'branch')
        search = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if search:
            queryset = queryset.filter(Q(client__name__icontains=search) | Q(insurance_company__name__icontains=search) | Q(branch__name__icontains=search))
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class ProposalDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = Proposal
    template_name = 'proposals/proposal_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_generate_policy'] = not hasattr(self.object, 'policy') and self.object.status != Proposal.STATUS_CONVERTED
        return context


class ProposalCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Nova proposta'}


class ProposalUpdateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, UpdateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar proposta'}


class ProposalDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = Proposal
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('proposals:list')


class ProposalCoveredItemCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, CreateView):
    form_class = CoveredItemForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Novo item da proposta'}

    def dispatch(self, request, *args, **kwargs):
        self.proposal = get_tenant_object_or_404(Proposal, request.brokerage, pk=kwargs['proposal_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.brokerage = self.request.brokerage
        form.instance.proposal = self.proposal
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('proposals:detail', kwargs={'pk': self.proposal.pk})


class ProposalCoverageCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, CreateView):
    model = Coverage
    form_class = CoverageForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Nova cobertura da proposta'}

    def dispatch(self, request, *args, **kwargs):
        self.proposal = get_tenant_object_or_404(Proposal, request.brokerage, pk=kwargs['proposal_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.brokerage = self.request.brokerage
        form.instance.proposal = self.proposal
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('proposals:detail', kwargs={'pk': self.proposal.pk})


class CoverageDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = Coverage
    template_name = 'generic/confirm_delete.html'

    def get_success_url(self):
        if self.object.proposal_id:
            return reverse('proposals:detail', kwargs={'pk': self.object.proposal_id})
        return reverse('proposals:list')
