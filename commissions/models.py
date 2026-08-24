from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class Agent(BrokerageModel):
    TYPE_PERSON = 'person'
    TYPE_COMPANY = 'company'
    TYPE_CHOICES = ((TYPE_PERSON, 'Pessoa física'), (TYPE_COMPANY, 'Empresa'))

    name = models.CharField('nome', max_length=200)
    document = models.CharField('documento', max_length=32, blank=True)
    type = models.CharField('tipo', max_length=20, choices=TYPE_CHOICES, default=TYPE_PERSON)
    commission_rate = models.DecimalField('percentual de comissão', max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'agente'
        verbose_name_plural = 'agentes'
        ordering = ('name',)
        indexes = [models.Index(fields=['brokerage', 'name'])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('commissions:agent_detail', kwargs={'pk': self.pk})


class Producer(BrokerageModel):
    agent = models.ForeignKey(Agent, verbose_name='agente', on_delete=models.SET_NULL, related_name='producers', null=True, blank=True)
    name = models.CharField('nome', max_length=200)
    document = models.CharField('documento', max_length=32, blank=True)
    commission_rate = models.DecimalField('percentual de comissão', max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'produtor'
        verbose_name_plural = 'produtores'
        ordering = ('name',)
        indexes = [models.Index(fields=['brokerage', 'name'])]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.agent and self.agent.brokerage_id != self.brokerage_id:
            raise ValidationError({'agent': 'Agente de outra corretora.'})

    def get_absolute_url(self):
        return reverse('commissions:producer_detail', kwargs={'pk': self.pk})


class Commission(BrokerageModel):
    STATUS_EXPECTED = 'expected'
    STATUS_RECEIVED = 'received'
    STATUS_PARTIALLY_PAID = 'partially_paid'
    STATUS_PAID = 'paid'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = (
        (STATUS_EXPECTED, 'Prevista'),
        (STATUS_RECEIVED, 'Recebida'),
        (STATUS_PARTIALLY_PAID, 'Parcialmente paga'),
        (STATUS_PAID, 'Paga'),
        (STATUS_CANCELLED, 'Cancelada'),
    )

    policy = models.ForeignKey('policies.Policy', verbose_name='apólice', on_delete=models.PROTECT, related_name='commissions')
    agent = models.ForeignKey(Agent, verbose_name='agente', on_delete=models.SET_NULL, related_name='commissions', null=True, blank=True)
    producer = models.ForeignKey(Producer, verbose_name='produtor', on_delete=models.SET_NULL, related_name='commissions', null=True, blank=True)
    gross_amount = models.DecimalField('comissão bruta', max_digits=12, decimal_places=2, default=0)
    brokerage_amount = models.DecimalField('valor da corretora', max_digits=12, decimal_places=2, default=0)
    agent_amount = models.DecimalField('valor do agente', max_digits=12, decimal_places=2, default=0)
    producer_amount = models.DecimalField('valor do produtor', max_digits=12, decimal_places=2, default=0)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default=STATUS_EXPECTED, db_index=True)

    class Meta:
        verbose_name = 'comissão'
        verbose_name_plural = 'comissões'
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['brokerage', 'status']), models.Index(fields=['brokerage', 'created_at'])]

    def __str__(self):
        return f'Comissão {self.policy}'

    def clean(self):
        super().clean()
        for field_name in ('policy', 'agent', 'producer'):
            value = getattr(self, field_name, None)
            if value and value.brokerage_id != self.brokerage_id:
                raise ValidationError({field_name: 'Este registro pertence a outra corretora.'})

    def calculate_amounts(self):
        agent_rate = self.agent.commission_rate if self.agent else Decimal('0')
        producer_rate = self.producer.commission_rate if self.producer else Decimal('0')
        self.agent_amount = self.gross_amount * agent_rate / Decimal('100')
        self.producer_amount = self.gross_amount * producer_rate / Decimal('100')
        self.brokerage_amount = self.gross_amount - self.agent_amount - self.producer_amount

    def save(self, *args, **kwargs):
        self.calculate_amounts()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('commissions:detail', kwargs={'pk': self.pk})
