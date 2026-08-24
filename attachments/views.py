from django.http import FileResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from base.models import BrokerageScopedFormKwargsMixin, TenantObjectMixin, TenantQuerySetMixin, get_tenant_object_or_404
from base.views import InternalViewMixin

from .forms import AttachmentForm
from .models import Attachment


class AttachmentListView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Attachment
    template_name = 'generic/object_list.html'
    context_object_name = 'objects'
    extra_context = {'title': 'Anexos', 'create_url_name': 'attachments:create'}


class AttachmentCreateView(InternalViewMixin, BrokerageScopedFormKwargsMixin, TenantObjectMixin, CreateView):
    model = Attachment
    form_class = AttachmentForm
    template_name = 'generic/form.html'
    extra_context = {'title': 'Novo anexo'}

    def form_valid(self, form):
        uploaded_file = form.cleaned_data['file']
        form.instance.uploaded_by = self.request.user
        form.instance.original_name = uploaded_file.name
        form.instance.content_type = getattr(uploaded_file, 'content_type', '') or ''
        form.instance.size_bytes = uploaded_file.size
        return super().form_valid(form)


class AttachmentDeleteView(InternalViewMixin, TenantQuerySetMixin, DeleteView):
    model = Attachment
    template_name = 'generic/confirm_delete.html'
    success_url = reverse_lazy('attachments:list')


class AttachmentDownloadView(InternalViewMixin, TenantQuerySetMixin, ListView):
    model = Attachment

    def get(self, request, pk):
        attachment = get_tenant_object_or_404(Attachment, request.brokerage, pk=pk)
        if not attachment.file:
            raise Http404('Arquivo não encontrado.')
        return FileResponse(attachment.file.open('rb'), as_attachment=True, filename=attachment.original_name or None)
