from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.models import BrokerageScopedFormKwargsMixin, TenantObjectMixin, TenantQuerySetMixin
from base.views import InternalViewMixin

from .forms import CoveredItemForm
from .models import CoveredItem


class CoveredItemListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = CoveredItem
    template_name = 'generic/object_list.html'
    context_object_name = 'objects'
    extra_context = {'title': 'Itens cobertos', 'create_url_name': 'covered_items:create'}

    def get_queryset(self):
        queryset = super().get_queryset().select_related('proposal')
        search = self.request.GET.get('q')
        item_type = self.request.GET.get('type')
        if search:
            queryset = queryset.filter(Q(description__icontains=search) | Q(proposal__client__name__icontains=search))
        if item_type:
            queryset = queryset.filter(item_type=item_type)
        return queryset


class CoveredItemDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = CoveredItem
    template_name = 'generic/detail.html'


class CoveredItemCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, CreateView):
    model = CoveredItem
    form_class = CoveredItemForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Novo item coberto'}


class CoveredItemUpdateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, UpdateView):
    model = CoveredItem
    form_class = CoveredItemForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar item coberto'}


class CoveredItemDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = CoveredItem
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('covered_items:list')
