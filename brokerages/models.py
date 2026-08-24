from django.db import models

from base.models import TimeStampedModel


class Brokerage(TimeStampedModel):
    PLAN_FREE = 'free'
    PLAN_CHOICES = ((PLAN_FREE, 'Free'),)

    name = models.CharField('nome', max_length=150)
    legal_name = models.CharField('razão social', max_length=200)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    plan = models.CharField('plano', max_length=20, choices=PLAN_CHOICES, default=PLAN_FREE)
    is_active = models.BooleanField('ativa', default=True)

    class Meta:
        verbose_name = 'corretora'
        verbose_name_plural = 'corretoras'
        ordering = ('name',)

    def __str__(self):
        return self.name
