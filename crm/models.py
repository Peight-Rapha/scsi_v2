from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class DealStage(BrokerageModel):
    name = models.CharField('nome', max_length=120)
    color = models.CharField('cor', max_length=20, default='#1947e5')
    position = models.PositiveIntegerField('posição', default=0)

    class Meta:
        verbose_name = 'etapa do CRM'
        verbose_name_plural = 'etapas do CRM'
        ordering = ('position', 'name')
        indexes = [models.Index(fields=['brokerage', 'position'])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('crm:kanban')


class Deal(BrokerageModel):
    STATUS_OPEN = 'open'
    STATUS_WON = 'won'
    STATUS_LOST = 'lost'
    STATUS_ARCHIVED = 'archived'
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Aberta'),
        (STATUS_WON, 'Ganha'),
        (STATUS_LOST, 'Perdida'),
        (STATUS_ARCHIVED, 'Arquivada'),
    )

    client = models.ForeignKey('clients.Client', verbose_name='cliente', on_delete=models.PROTECT, related_name='deals')
    stage = models.ForeignKey(DealStage, verbose_name='etapa', on_delete=models.PROTECT, related_name='deals')
    title = models.CharField('título', max_length=200)
    estimated_value = models.DecimalField('valor estimado', max_digits=12, decimal_places=2, default=0)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN, db_index=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='responsável', on_delete=models.PROTECT, related_name='deals', null=True, blank=True)
    ai_summary = models.TextField('resumo IA', blank=True)

    class Meta:
        verbose_name = 'negociação'
        verbose_name_plural = 'negociações'
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['brokerage', 'status']), models.Index(fields=['brokerage', 'assigned_to'])]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.client and self.client.brokerage_id != self.brokerage_id:
            raise ValidationError({'client': 'Cliente de outra corretora.'})
        if self.stage and self.stage.brokerage_id != self.brokerage_id:
            raise ValidationError({'stage': 'Etapa de outra corretora.'})
        if self.assigned_to and self.assigned_to.brokerage_id != self.brokerage_id:
            raise ValidationError({'assigned_to': 'Responsável de outra corretora.'})

    def get_absolute_url(self):
        return reverse('crm:detail', kwargs={'pk': self.pk})
