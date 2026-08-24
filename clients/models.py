from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class Client(BrokerageModel):
    TYPE_INDIVIDUAL = 'individual'
    TYPE_COMPANY = 'company'
    TYPE_CHOICES = ((TYPE_INDIVIDUAL, 'Pessoa física'), (TYPE_COMPANY, 'Pessoa jurídica'))

    name = models.CharField('nome', max_length=200)
    document = models.CharField('documento', max_length=32, blank=True)
    email = models.EmailField('email', blank=True)
    phone = models.CharField('telefone', max_length=32, blank=True)
    type = models.CharField('tipo', max_length=20, choices=TYPE_CHOICES, default=TYPE_INDIVIDUAL)
    notes = models.TextField('observações', blank=True)
    ai_summary = models.TextField('resumo IA', blank=True)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        ordering = ('name',)
        indexes = [models.Index(fields=['brokerage', 'name']), models.Index(fields=['brokerage', 'created_at'])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clients:detail', kwargs={'pk': self.pk})
