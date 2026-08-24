from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.models import TenantObjectMixin, TenantQuerySetMixin
from base.views import InternalViewMixin

from .forms import InsuranceBranchForm
from .models import InsuranceBranch


class InsuranceBranchListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = InsuranceBranch
    template_name = 'generic/object_list.html'
    context_object_name = 'objects'
    extra_context = {'title': 'Ramos de seguro', 'create_url_name': 'branches:create'}

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return queryset


class InsuranceBranchDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = InsuranceBranch
    template_name = 'generic/detail.html'


class InsuranceBranchCreateView(InternalViewMixin, TenantObjectMixin, CreateView):
    model = InsuranceBranch
    form_class = InsuranceBranchForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Novo ramo'}


class InsuranceBranchUpdateView(InternalViewMixin, TenantObjectMixin, UpdateView):
    model = InsuranceBranch
    form_class = InsuranceBranchForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar ramo'}


class InsuranceBranchDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = InsuranceBranch
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('branches:list')
