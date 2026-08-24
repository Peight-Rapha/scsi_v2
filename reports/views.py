import csv
from io import BytesIO

from django.http import FileResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView

from base.views import InternalViewMixin
from claims.models import Claim
from clients.models import Client
from commissions.models import Commission
from policies.models import Policy
from proposals.models import Proposal
from renewals.models import Renewal


REPORTS = {
    'clients': ('Clientes', Client, ('name', 'document', 'email', 'phone')),
    'policies': ('Apólices', Policy, ('policy_number', 'client', 'status', 'premium_amount')),
    'proposals': ('Propostas', Proposal, ('client', 'status', 'premium_amount', 'valid_until')),
    'claims': ('Sinistros', Claim, ('claim_number', 'client', 'policy', 'status')),
    'renewals': ('Renovações', Renewal, ('policy', 'due_date', 'status', 'notes')),
    'commissions': ('Comissões', Commission, ('policy', 'status', 'gross_amount', 'brokerage_amount', 'agent_amount', 'producer_amount')),
}


def get_report_queryset(slug, brokerage):
    title, model, fields = REPORTS[slug]
    return title, fields, model.objects.for_brokerage(brokerage)


class ReportsIndexView(InternalViewMixin, TemplateView):
    template_name = 'reports/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = [(slug, config[0]) for slug, config in REPORTS.items()]
        return context


class ReportCSVView(InternalViewMixin, View):
    def get(self, request, slug):
        if slug not in REPORTS:
            return HttpResponse('Relatório não encontrado.', status=404)
        title, fields, queryset = get_report_queryset(slug, request.brokerage)
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{slug}.csv"'
        writer = csv.writer(response)
        writer.writerow([field.replace('_', ' ').title() for field in fields])
        for item in queryset:
            writer.writerow([str(getattr(item, field, '')) for field in fields])
        return response


class ReportPDFView(InternalViewMixin, View):
    def get(self, request, slug):
        if slug not in REPORTS:
            return HttpResponse('Relatório não encontrado.', status=404)
        title, fields, queryset = get_report_queryset(slug, request.brokerage)
        buffer = BytesIO()
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
        except ImportError:
            return HttpResponse('ReportLab não está instalado neste ambiente.', status=503)
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 50
        pdf.setFont('Helvetica-Bold', 14)
        pdf.drawString(40, y, f'Relatório de {title}')
        pdf.setFont('Helvetica', 9)
        y -= 30
        for item in queryset[:200]:
            line = ' | '.join(str(getattr(item, field, '')) for field in fields)
            pdf.drawString(40, y, line[:120])
            y -= 16
            if y < 40:
                pdf.showPage()
                y = height - 50
        pdf.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'{slug}.pdf')
