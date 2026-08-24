from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from base.models import BrokerageScopedFormKwargsMixin, TenantObjectMixin, TenantQuerySetMixin
from base.views import InternalViewMixin

from .forms import AgentForm, CommissionForm, ProducerForm
from .models import Agent, Commission, Producer


class CommissionListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'
    context_object_name = 'commissions'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('policy', 'agent', 'producer')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        totals = self.get_queryset().aggregate(gross=Sum('gross_amount'), brokerage=Sum('brokerage_amount'), agent=Sum('agent_amount'), producer=Sum('producer_amount'))
        context['totals'] = {key: value or 0 for key, value in totals.items()}
        return context


class CommissionDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = Commission
    template_name = 'generic/detail.html'


class CommissionCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Nova comissão'}


class CommissionUpdateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar comissão'}


class CommissionDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = Commission
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('commissions:list')


class AgentListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Agent
    template_name = 'generic/object_list.html'
    context_object_name = 'objects'
    extra_context = {'title': 'Agentes', 'create_url_name': 'commissions:agent_create'}

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(document__icontains=search))
        return queryset


class AgentDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = Agent
    template_name = 'generic/detail.html'


class AgentCreateView(InternalViewMixin, TenantObjectMixin, CreateView):
    model = Agent
    form_class = AgentForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Novo agente'}


class AgentUpdateView(InternalViewMixin, TenantObjectMixin, UpdateView):
    model = Agent
    form_class = AgentForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar agente'}


class ProducerListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Producer
    template_name = 'generic/object_list.html'
    context_object_name = 'objects'
    extra_context = {'title': 'Produtores', 'create_url_name': 'commissions:producer_create'}


class ProducerDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = Producer
    template_name = 'generic/detail.html'


class ProducerCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, CreateView):
    model = Producer
    form_class = ProducerForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Novo produtor'}


class ProducerUpdateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, UpdateView):
    model = Producer
    form_class = ProducerForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar produtor'}
