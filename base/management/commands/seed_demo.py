from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from branches.models import InsuranceBranch
from brokerages.models import Brokerage
from claims.models import Claim
from clients.models import Client
from commissions.models import Agent, Commission, Producer
from covered_items.models import CoveredItem
from crm.models import Deal, DealStage
from insurers.models import InsuranceCompany
from policies.models import Policy
from proposals.models import Proposal
from renewals.models import Renewal


class Command(BaseCommand):
    help = 'Cria dados fake de demonstração multi-tenant.'

    def handle(self, *args, **options):
        User = get_user_model()
        today = timezone.localdate()
        for index in range(1, 4):
            brokerage, _ = Brokerage.objects.get_or_create(cnpj=f'00.000.000/000{index}-00', defaults={'name': f'Demo Corretora {index}', 'legal_name': f'Demonstração Corretora {index} Ltda', 'plan': Brokerage.PLAN_FREE})
            user, _ = User.objects.get_or_create(email=f'demo{index}@scsi.digital', defaults={'first_name': 'Usuário', 'last_name': 'Demo', 'brokerage': brokerage})
            user.brokerage = brokerage
            user.set_password('demo123456')
            user.save()
            insurer, _ = InsuranceCompany.objects.get_or_create(brokerage=brokerage, name='Demo Seguradora', defaults={'cnpj': f'11.111.111/000{index}-00'})
            branch, _ = InsuranceBranch.objects.get_or_create(brokerage=brokerage, name='Automóvel')
            agent, _ = Agent.objects.get_or_create(brokerage=brokerage, name='Agente Demo', defaults={'type': Agent.TYPE_PERSON, 'commission_rate': Decimal('10')})
            producer, _ = Producer.objects.get_or_create(brokerage=brokerage, name='Produtor Demo', defaults={'agent': agent, 'commission_rate': Decimal('5')})
            stage, _ = DealStage.objects.get_or_create(brokerage=brokerage, name='Novo lead', defaults={'color': '#1947e5', 'position': 1})
            for number in range(1, 6):
                client, _ = Client.objects.get_or_create(brokerage=brokerage, name=f'Cliente Demo {index}.{number}', defaults={'document': f'DEMO-{index}-{number}', 'email': f'cliente{index}{number}@example.com', 'notes': 'Registro de demonstração.'})
                proposal, _ = Proposal.objects.get_or_create(brokerage=brokerage, client=client, insurance_company=insurer, branch=branch, defaults={'status': Proposal.STATUS_APPROVED, 'premium_amount': Decimal('1200.00'), 'commission_rate': Decimal('20.00'), 'valid_until': today + timedelta(days=30)})
                policy, _ = Policy.objects.get_or_create(brokerage=brokerage, client=client, insurance_company=insurer, branch=branch, policy_number=f'DEMO-{index}-{number}', defaults={'proposal': proposal, 'start_date': today - timedelta(days=30), 'end_date': today + timedelta(days=330), 'premium_amount': proposal.premium_amount, 'status': Policy.STATUS_ACTIVE})
                item, _ = CoveredItem.objects.get_or_create(brokerage=brokerage, policy_id=policy.pk, description=f'Veículo demo {number}', defaults={'item_type': CoveredItem.TYPE_VEHICLE, 'insured_value': Decimal('65000.00')})
                Claim.objects.get_or_create(brokerage=brokerage, client=client, policy=policy, covered_item=item, claim_number=f'SIN-DEMO-{index}-{number}', defaults={'status': Claim.STATUS_REPORTED, 'occurred_at': today - timedelta(days=number), 'description': 'Sinistro de demonstração.'})
                Renewal.objects.get_or_create(brokerage=brokerage, policy=policy, defaults={'due_date': today + timedelta(days=30 * number), 'status': Renewal.STATUS_PENDING, 'notes': 'Renovação de demonstração.'})
                Commission.objects.get_or_create(brokerage=brokerage, policy=policy, defaults={'agent': agent, 'producer': producer, 'gross_amount': Decimal('240.00'), 'status': Commission.STATUS_EXPECTED})
                Deal.objects.get_or_create(brokerage=brokerage, client=client, stage=stage, title=f'Negociação Demo {number}', defaults={'estimated_value': Decimal('1500.00'), 'assigned_to': user})
        self.stdout.write(self.style.SUCCESS('Dados fake de demonstração criados.'))
