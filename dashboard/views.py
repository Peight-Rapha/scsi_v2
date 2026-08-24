from datetime import timedelta

from django.db.models import Count, Sum
from django.utils import timezone
from django.views.generic import TemplateView

from base.views import InternalViewMixin
from claims.models import Claim
from clients.models import Client
from commissions.models import Commission
from crm.models import Deal, DealStage
from insurers.models import InsuranceCompany
from policies.models import Policy
from proposals.models import Proposal
from renewals.models import Renewal


class DashboardView(InternalViewMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brokerage = self.request.brokerage
        today = timezone.localdate()
        context['metrics'] = {
            'clients': Client.objects.for_brokerage(brokerage).count(),
            'active_policies': Policy.objects.for_brokerage(brokerage).filter(status=Policy.STATUS_ACTIVE).count(),
            'open_claims': Claim.objects.for_brokerage(brokerage).exclude(status=Claim.STATUS_CLOSED).count(),
            'premium': Policy.objects.for_brokerage(brokerage).aggregate(total=Sum('premium_amount'))['total'] or 0,
            'expected_commissions': Commission.objects.for_brokerage(brokerage).aggregate(total=Sum('gross_amount'))['total'] or 0,
            'renewals_30': Renewal.objects.for_brokerage(brokerage).filter(due_date__gte=today, due_date__lte=today + timedelta(days=30)).count(),
            'proposals': Proposal.objects.for_brokerage(brokerage).count(),
            'insurers': InsuranceCompany.objects.for_brokerage(brokerage).count(),
        }
        context['deals_by_stage'] = DealStage.objects.for_brokerage(brokerage).annotate(total=Count('deals'), value=Sum('deals__estimated_value'))
        context['policies_by_status'] = Policy.objects.for_brokerage(brokerage).values('status').annotate(total=Count('id')).order_by('status')
        return context
