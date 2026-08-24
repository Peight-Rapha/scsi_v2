from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class CoveredItem(BrokerageModel):
    TYPE_VEHICLE = 'vehicle'
    TYPE_PROPERTY = 'property'
    TYPE_LIFE = 'life'
    TYPE_TRAVEL = 'travel'
    TYPE_BUSINESS = 'business'
    TYPE_OTHER = 'other'
    TYPE_CHOICES = (
        (TYPE_VEHICLE, 'Veículo'),
        (TYPE_PROPERTY, 'Imóvel'),
        (TYPE_LIFE, 'Vida'),
        (TYPE_TRAVEL, 'Viagem'),
        (TYPE_BUSINESS, 'Empresarial'),
        (TYPE_OTHER, 'Outro'),
    )

    proposal = models.ForeignKey('proposals.Proposal', verbose_name='proposta', on_delete=models.CASCADE, related_name='covered_items', null=True, blank=True)
    policy_id = models.PositiveBigIntegerField('ID da apólice', null=True, blank=True)
    item_type = models.CharField('tipo', max_length=20, choices=TYPE_CHOICES, default=TYPE_OTHER)
    description = models.TextField('descrição')
    insured_value = models.DecimalField('valor segurado', max_digits=12, decimal_places=2, default=0)
    metadata = models.JSONField('metadados', default=dict, blank=True)

    class Meta:
        verbose_name = 'item coberto'
        verbose_name_plural = 'itens cobertos'
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['brokerage', 'item_type']), models.Index(fields=['brokerage', 'created_at'])]

    def __str__(self):
        return self.description[:80]

    def clean(self):
        super().clean()
        if not self.proposal_id and not self.policy_id:
            raise ValidationError('Informe uma proposta ou uma apólice.')
        if self.proposal and self.proposal.brokerage_id != self.brokerage_id:
            raise ValidationError('A proposta deve pertencer à mesma corretora.')

    def get_absolute_url(self):
        return reverse('covered_items:detail', kwargs={'pk': self.pk})
