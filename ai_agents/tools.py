from claims.models import Claim
from clients.models import Client
from crm.models import Deal
from policies.models import Policy
from proposals.models import Proposal


ENTITY_MODELS = {
    'client': Client,
    'proposal': Proposal,
    'policy': Policy,
    'claim': Claim,
    'deal': Deal,
}


def get_entity_for_brokerage(entity_type, entity_id, brokerage):
    model = ENTITY_MODELS[entity_type]
    return model.objects.for_brokerage(brokerage).get(pk=entity_id)


def build_entity_context(entity_type, entity):
    if entity_type == 'client':
        return f'Cliente: {entity.name}\nDocumento: {entity.document}\nEmail: {entity.email}\nObservações: {entity.notes}'
    if entity_type == 'proposal':
        return f'Proposta: {entity}\nCliente: {entity.client}\nStatus: {entity.get_status_display()}\nPrêmio: {entity.premium_amount}'
    if entity_type == 'policy':
        return f'Apólice: {entity.policy_number}\nCliente: {entity.client}\nStatus: {entity.get_status_display()}\nPrêmio: {entity.premium_amount}'
    if entity_type == 'claim':
        return f'Sinistro: {entity.claim_number}\nCliente: {entity.client}\nStatus: {entity.get_status_display()}\nDescrição: {entity.description}'
    if entity_type == 'deal':
        return f'Negociação: {entity.title}\nCliente: {entity.client}\nEtapa: {entity.stage}\nValor estimado: {entity.estimated_value}'
    return str(entity)


def tenant_snapshot(brokerage):
    return {
        'clients': Client.objects.for_brokerage(brokerage).count(),
        'proposals': Proposal.objects.for_brokerage(brokerage).count(),
        'policies': Policy.objects.for_brokerage(brokerage).count(),
        'claims': Claim.objects.for_brokerage(brokerage).count(),
        'deals': Deal.objects.for_brokerage(brokerage).count(),
    }
