from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.models import TenantObjectMixin, TenantQuerySetMixin
from base.views import InternalViewMixin

from .forms import InsuranceCompanyForm
from .models import InsuranceCompany


class InsuranceCompanyListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = InsuranceCompany
    template_name = 'generic/object_list.html'
    context_object_name = 'objects'
    extra_context = {'title': 'Seguradoras', 'create_url_name': 'insurers:create'}

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(cnpj__icontains=search))
        return queryset


class InsuranceCompanyDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = InsuranceCompany
    template_name = 'generic/detail.html'


class InsuranceCompanyCreateView(InternalViewMixin, TenantObjectMixin, CreateView):
    model = InsuranceCompany
    form_class = InsuranceCompanyForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Nova seguradora'}


class InsuranceCompanyUpdateView(InternalViewMixin, TenantObjectMixin, UpdateView):
    model = InsuranceCompany
    form_class = InsuranceCompanyForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar seguradora'}


class InsuranceCompanyDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = InsuranceCompany
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('insurers:list')
