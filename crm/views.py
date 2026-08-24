from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from base.models import BrokerageScopedFormKwargsMixin, TenantObjectMixin, TenantQuerySetMixin, get_tenant_object_or_404
from base.views import InternalViewMixin

from .forms import DealForm, DealStageForm
from .models import Deal, DealStage


class DealListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Deal
    template_name = 'crm/deal_list.html'
    context_object_name = 'deals'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('client', 'stage', 'assigned_to')
        search = self.request.GET.get('q')
        status = self.request.GET.get('status')
        stage = self.request.GET.get('stage')
        assigned_to = self.request.GET.get('assigned_to')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(client__name__icontains=search))
        if status:
            queryset = queryset.filter(status=status)
        if stage:
            queryset = queryset.filter(stage_id=stage)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        return queryset


class DealDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = Deal
    template_name = 'crm/deal_detail.html'


class DealCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, CreateView):
    model = Deal
    form_class = DealForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Nova negociação'}


class DealUpdateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, UpdateView):
    model = Deal
    form_class = DealForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar negociação'}


class DealDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = Deal
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('crm:list')


class DealStageCreateView(InternalViewMixin, TenantObjectMixin, CreateView):
    model = DealStage
    form_class = DealStageForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Nova etapa'}
    success_url = reverse_lazy('crm:kanban')


class DealStageUpdateView(InternalViewMixin, TenantObjectMixin, UpdateView):
    model = DealStage
    form_class = DealStageForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar etapa'}
    success_url = reverse_lazy('crm:kanban')

    def get_queryset(self):
        return DealStage.objects.for_brokerage(self.request.brokerage)


class DealKanbanView(InternalViewMixin, TemplateView):
    template_name = 'crm/kanban.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stages = DealStage.objects.for_brokerage(self.request.brokerage).prefetch_related('deals')
        context['stages'] = stages
        context['deals_by_stage'] = {stage.pk: Deal.objects.for_brokerage(self.request.brokerage).filter(stage=stage).select_related('client') for stage in stages}
        return context


class MoveDealStageView(InternalViewMixin, View):
    def post(self, request, pk):
        deal = get_tenant_object_or_404(Deal, request.brokerage, pk=pk)
        stage = get_tenant_object_or_404(DealStage, request.brokerage, pk=request.POST.get('stage'))
        deal.stage = stage
        deal.full_clean()
        deal.save(update_fields=['stage', 'updated_at'])
        return redirect('crm:kanban')
