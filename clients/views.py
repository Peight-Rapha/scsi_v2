from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.models import TenantObjectMixin, TenantQuerySetMixin
from base.views import InternalViewMixin

from .forms import ClientForm
from .models import Client


class ClientListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        client_type = self.request.GET.get('type')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(document__icontains=search) | Q(email__icontains=search))
        if client_type:
            queryset = queryset.filter(type=client_type)
        return queryset


class ClientDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'


class ClientCreateView(InternalViewMixin, TenantObjectMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Novo cliente'}


class ClientUpdateView(InternalViewMixin, TenantObjectMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar cliente'}


class ClientDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = Client
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('clients:list')
