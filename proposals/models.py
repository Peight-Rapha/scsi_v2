from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class Proposal(BrokerageModel):
    STATUS_DRAFT = 'draft'
    STATUS_SENT = 'sent'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CONVERTED = 'converted'
    STATUS_EXPIRED = 'expired'
    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Rascunho'),
        (STATUS_SENT, 'Enviada'),
        (STATUS_APPROVED, 'Aprovada'),
        (STATUS_REJECTED, 'Rejeitada'),
        (STATUS_CONVERTED, 'Convertida'),
        (STATUS_EXPIRED, 'Expirada'),
    )

    client = models.ForeignKey('clients.Client', verbose_name='cliente', on_delete=models.PROTECT, related_name='proposals')
    insurance_company = models.ForeignKey('insurers.InsuranceCompany', verbose_name='seguradora', on_delete=models.PROTECT, related_name='proposals', null=True, blank=True)
    branch = models.ForeignKey('branches.InsuranceBranch', verbose_name='ramo', on_delete=models.PROTECT, related_name='proposals', null=True, blank=True)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT, db_index=True)
    premium_amount = models.DecimalField('prêmio', max_digits=12, decimal_places=2, default=0)
    commission_rate = models.DecimalField('percentual de comissão', max_digits=5, decimal_places=2, default=0)
    valid_until = models.DateField('válida até', null=True, blank=True)
    ai_summary = models.TextField('resumo IA', blank=True)

    class Meta:
        verbose_name = 'proposta'
        verbose_name_plural = 'propostas'
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['brokerage', 'status']), models.Index(fields=['brokerage', 'created_at'])]

    def __str__(self):
        return f'Proposta #{self.pk} - {self.client}'

    def clean(self):
        super().clean()
        tenant_fields = ('client', 'insurance_company', 'branch')
        for field_name in tenant_fields:
            value = getattr(self, field_name, None)
            if value and value.brokerage_id != self.brokerage_id:
                raise ValidationError({field_name: 'Este registro pertence a outra corretora.'})

    def get_absolute_url(self):
        return reverse('proposals:detail', kwargs={'pk': self.pk})


class Coverage(BrokerageModel):
    proposal = models.ForeignKey(Proposal, verbose_name='proposta', on_delete=models.CASCADE, related_name='coverages', null=True, blank=True)
    policy_id = models.PositiveBigIntegerField('ID da apólice', null=True, blank=True)
    name = models.CharField('nome', max_length=150)
    limit_amount = models.DecimalField('limite', max_digits=12, decimal_places=2, default=0)
    deductible_amount = models.DecimalField('franquia', max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'cobertura'
        verbose_name_plural = 'coberturas'
        ordering = ('name',)
        indexes = [models.Index(fields=['brokerage', 'name'])]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if not self.proposal_id and not self.policy_id:
            raise ValidationError('Informe uma proposta ou uma apólice.')
        if self.proposal and self.proposal.brokerage_id != self.brokerage_id:
            raise ValidationError('A proposta deve pertencer à mesma corretora.')
