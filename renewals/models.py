from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from base.models import BrokerageModel


class Renewal(BrokerageModel):
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RENEWED = 'renewed'
    STATUS_LOST = 'lost'
    STATUS_EXPIRED = 'expired'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pendente'),
        (STATUS_IN_PROGRESS, 'Em andamento'),
        (STATUS_RENEWED, 'Renovada'),
        (STATUS_LOST, 'Perdida'),
        (STATUS_EXPIRED, 'Expirada'),
    )

    policy = models.ForeignKey('policies.Policy', verbose_name='apólice', on_delete=models.CASCADE, related_name='renewals')
    due_date = models.DateField('vencimento', db_index=True)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    notes = models.TextField('observações', blank=True)

    class Meta:
        verbose_name = 'renovação'
        verbose_name_plural = 'renovações'
        ordering = ('due_date',)
        indexes = [models.Index(fields=['brokerage', 'due_date']), models.Index(fields=['brokerage', 'status'])]

    def __str__(self):
        return f'Renovação {self.policy} - {self.due_date}'

    def clean(self):
        super().clean()
        if self.policy and self.policy.brokerage_id != self.brokerage_id:
            raise ValidationError({'policy': 'A apólice pertence a outra corretora.'})

    @property
    def is_due_soon(self):
        today = timezone.localdate()
        return today <= self.due_date <= today + timedelta(days=30)

    def get_absolute_url(self):
        return reverse('renewals:detail', kwargs={'pk': self.pk})
