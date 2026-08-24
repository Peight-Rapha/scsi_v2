from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class InsuranceCompany(BrokerageModel):
    name = models.CharField('nome', max_length=200)
    cnpj = models.CharField('CNPJ', max_length=18, blank=True)
    contact_email = models.EmailField('email de contato', blank=True)
    contact_phone = models.CharField('telefone de contato', max_length=32, blank=True)

    class Meta:
        verbose_name = 'seguradora'
        verbose_name_plural = 'seguradoras'
        ordering = ('name',)
        indexes = [models.Index(fields=['brokerage', 'name'])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('insurers:detail', kwargs={'pk': self.pk})
