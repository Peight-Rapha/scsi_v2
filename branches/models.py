from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class InsuranceBranch(BrokerageModel):
    name = models.CharField('nome', max_length=150)
    description = models.TextField('descrição', blank=True)

    class Meta:
        verbose_name = 'ramo de seguro'
        verbose_name_plural = 'ramos de seguro'
        ordering = ('name',)
        indexes = [models.Index(fields=['brokerage', 'name'])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('branches:detail', kwargs={'pk': self.pk})
