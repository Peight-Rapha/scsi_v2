from django.db import transaction

from covered_items.models import CoveredItem
from proposals.models import Coverage, Proposal

from .models import Policy


@transaction.atomic
def generate_policy_from_proposal(proposal, policy_number=None):
    if hasattr(proposal, 'policy'):
        raise ValueError('Esta proposta já gerou uma apólice.')
    if proposal.status == Proposal.STATUS_CONVERTED:
        raise ValueError('Esta proposta já está convertida.')

    policy = Policy.objects.create(
        brokerage=proposal.brokerage,
        proposal=proposal,
        client=proposal.client,
        insurance_company=proposal.insurance_company,
        branch=proposal.branch,
        policy_number=policy_number or f'POL-{proposal.brokerage_id}-{proposal.pk}',
        premium_amount=proposal.premium_amount,
        status=Policy.STATUS_PENDING,
        ai_summary=proposal.ai_summary,
    )

    for item in proposal.covered_items.all():
        CoveredItem.objects.create(
            brokerage=proposal.brokerage,
            policy_id=policy.pk,
            item_type=item.item_type,
            description=item.description,
            insured_value=item.insured_value,
            metadata=item.metadata,
        )

    for coverage in proposal.coverages.all():
        Coverage.objects.create(
            brokerage=proposal.brokerage,
            policy_id=policy.pk,
            name=coverage.name,
            limit_amount=coverage.limit_amount,
            deductible_amount=coverage.deductible_amount,
        )

    proposal.status = Proposal.STATUS_CONVERTED
    proposal.save(update_fields=['status', 'updated_at'])
    return policy
