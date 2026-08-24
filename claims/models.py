from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class Claim(BrokerageModel):
    STATUS_REPORTED = 'reported'
    STATUS_UNDER_REVIEW = 'under_review'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_PAID = 'paid'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = (
        (STATUS_REPORTED, 'Avisado'),
        (STATUS_UNDER_REVIEW, 'Em análise'),
        (STATUS_APPROVED, 'Aprovado'),
        (STATUS_REJECTED, 'Rejeitado'),
        (STATUS_PAID, 'Pago'),
        (STATUS_CLOSED, 'Encerrado'),
    )

    client = models.ForeignKey('clients.Client', verbose_name='cliente', on_delete=models.PROTECT, related_name='claims')
    policy = models.ForeignKey('policies.Policy', verbose_name='apólice', on_delete=models.PROTECT, related_name='claims')
    covered_item = models.ForeignKey('covered_items.CoveredItem', verbose_name='item coberto', on_delete=models.PROTECT, related_name='claims')
    claim_number = models.CharField('número do sinistro', max_length=80)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default=STATUS_REPORTED, db_index=True)
    occurred_at = models.DateField('data da ocorrência', null=True, blank=True)
    description = models.TextField('descrição')
    ai_summary = models.TextField('resumo IA', blank=True)

    class Meta:
        verbose_name = 'sinistro'
        verbose_name_plural = 'sinistros'
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['brokerage', 'status']), models.Index(fields=['brokerage', 'occurred_at'])]

    def __str__(self):
        return self.claim_number

    def clean(self):
        super().clean()
        for field_name in ('client', 'policy', 'covered_item'):
            value = getattr(self, field_name, None)
            if value and value.brokerage_id != self.brokerage_id:
                raise ValidationError({field_name: 'Este registro pertence a outra corretora.'})
        if self.policy_id and self.client_id and self.policy.client_id != self.client_id:
            raise ValidationError({'client': 'O cliente deve ser o mesmo da apólice.'})
        if self.policy_id and self.covered_item_id and self.covered_item.policy_id != self.policy_id:
            raise ValidationError({'covered_item': 'O item coberto deve pertencer à apólice.'})

    def get_absolute_url(self):
        return reverse('claims:detail', kwargs={'pk': self.pk})
