from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from base.models import BrokerageScopedFormKwargsMixin, TenantObjectMixin, TenantQuerySetMixin
from base.views import InternalViewMixin

from .forms import EndorsementForm
from .models import Endorsement


class EndorsementListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Endorsement
    template_name = 'generic/object_list.html'
    context_object_name = 'objects'
    extra_context = {'title': 'Endossos', 'create_url_name': 'endorsements:create'}

    def get_queryset(self):
        queryset = super().get_queryset().select_related('policy')
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(Q(endorsement_number__icontains=search) | Q(policy__policy_number__icontains=search))
        return queryset


class EndorsementDetailView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = Endorsement
    template_name = 'generic/detail.html'


class EndorsementCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, CreateView):
    model = Endorsement
    form_class = EndorsementForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Novo endosso'}


class EndorsementUpdateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, UpdateView):
    model = Endorsement
    form_class = EndorsementForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Editar endosso'}


class EndorsementDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = Endorsement
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('endorsements:list')
