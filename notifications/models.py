from django.conf import settings
from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class Notification(BrokerageModel):
    LEVEL_INFO = 'info'
    LEVEL_SUCCESS = 'success'
    LEVEL_WARNING = 'warning'
    LEVEL_ERROR = 'error'
    LEVEL_CHOICES = (
        (LEVEL_INFO, 'Informação'),
        (LEVEL_SUCCESS, 'Sucesso'),
        (LEVEL_WARNING, 'Atenção'),
        (LEVEL_ERROR, 'Erro'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField('título', max_length=180)
    message = models.TextField('mensagem')
    level = models.CharField('nível', max_length=20, choices=LEVEL_CHOICES, default=LEVEL_INFO)
    is_read = models.BooleanField('lida', default=False, db_index=True)

    class Meta:
        verbose_name = 'notificação'
        verbose_name_plural = 'notificações'
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['brokerage', 'user', 'is_read'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notifications:list')
