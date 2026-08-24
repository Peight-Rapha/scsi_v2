from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class Endorsement(BrokerageModel):
    TYPE_CHANGE = 'change'
    TYPE_CANCELLATION = 'cancellation'
    TYPE_ADDITION = 'addition'
    TYPE_CORRECTION = 'correction'
    TYPE_CHOICES = (
        (TYPE_CHANGE, 'Alteração'),
        (TYPE_CANCELLATION, 'Cancelamento'),
        (TYPE_ADDITION, 'Inclusão'),
        (TYPE_CORRECTION, 'Correção'),
    )

    policy = models.ForeignKey('policies.Policy', verbose_name='apólice', on_delete=models.CASCADE, related_name='endorsements')
    endorsement_number = models.CharField('número do endosso', max_length=80)
    type = models.CharField('tipo', max_length=20, choices=TYPE_CHOICES, default=TYPE_CHANGE)
    description = models.TextField('descrição')
    effective_date = models.DateField('data de vigência')

    class Meta:
        verbose_name = 'endosso'
        verbose_name_plural = 'endossos'
        ordering = ('-effective_date', '-created_at')
        indexes = [models.Index(fields=['brokerage', 'effective_date'])]
        constraints = [models.UniqueConstraint(fields=['brokerage', 'policy', 'endorsement_number'], name='unique_endorsement_per_policy')]

    def __str__(self):
        return f'Endosso {self.endorsement_number}'

    def clean(self):
        super().clean()
        if self.policy and self.policy.brokerage_id != self.brokerage_id:
            raise ValidationError({'policy': 'A apólice pertence a outra corretora.'})

    def get_absolute_url(self):
        return reverse('endorsements:detail', kwargs={'pk': self.pk})
