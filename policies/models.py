from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class Policy(BrokerageModel):
    STATUS_ACTIVE = 'active'
    STATUS_EXPIRED = 'expired'
    STATUS_CANCELLED = 'cancelled'
    STATUS_PENDING = 'pending'
    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Ativa'),
        (STATUS_EXPIRED, 'Vencida'),
        (STATUS_CANCELLED, 'Cancelada'),
        (STATUS_PENDING, 'Pendente'),
    )

    proposal = models.OneToOneField('proposals.Proposal', verbose_name='proposta', on_delete=models.PROTECT, related_name='policy', null=True, blank=True)
    client = models.ForeignKey('clients.Client', verbose_name='cliente', on_delete=models.PROTECT, related_name='policies')
    insurance_company = models.ForeignKey('insurers.InsuranceCompany', verbose_name='seguradora', on_delete=models.PROTECT, related_name='policies', null=True, blank=True)
    branch = models.ForeignKey('branches.InsuranceBranch', verbose_name='ramo', on_delete=models.PROTECT, related_name='policies', null=True, blank=True)
    policy_number = models.CharField('número da apólice', max_length=80)
    start_date = models.DateField('início de vigência', null=True, blank=True)
    end_date = models.DateField('fim de vigência', null=True, blank=True, db_index=True)
    premium_amount = models.DecimalField('prêmio', max_digits=12, decimal_places=2, default=0)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    ai_summary = models.TextField('resumo IA', blank=True)

    class Meta:
        verbose_name = 'apólice'
        verbose_name_plural = 'apólices'
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['brokerage', 'status']), models.Index(fields=['brokerage', 'end_date'])]
        constraints = [models.UniqueConstraint(fields=['brokerage', 'insurance_company', 'policy_number'], name='unique_policy_number_per_brokerage_insurer')]

    def __str__(self):
        return self.policy_number

    def clean(self):
        super().clean()
        for field_name in ('proposal', 'client', 'insurance_company', 'branch'):
            value = getattr(self, field_name, None)
            if value and value.brokerage_id != self.brokerage_id:
                raise ValidationError({field_name: 'Este registro pertence a outra corretora.'})

    def get_absolute_url(self):
        return reverse('policies:detail', kwargs={'pk': self.pk})

    @property
    def covered_items(self):
        from covered_items.models import CoveredItem

        return CoveredItem.objects.for_brokerage(self.brokerage).filter(policy_id=self.pk)

    @property
    def coverages(self):
        from proposals.models import Coverage

        return Coverage.objects.for_brokerage(self.brokerage).filter(policy_id=self.pk)
