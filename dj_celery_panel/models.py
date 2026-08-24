from django.db import models

from base.models import TimeStampedModel


class CeleryTaskEvent(TimeStampedModel):
    STATUS_STARTED = 'started'
    STATUS_SUCCESS = 'success'
    STATUS_FAILURE = 'failure'
    STATUS_CHOICES = (
        (STATUS_STARTED, 'Iniciada'),
        (STATUS_SUCCESS, 'Concluída'),
        (STATUS_FAILURE, 'Falhou'),
    )

    task_name = models.CharField('task', max_length=200)
    task_id = models.CharField('ID da task', max_length=120, blank=True)
    brokerage_id = models.PositiveBigIntegerField('ID da corretora', null=True, blank=True)
    user_id = models.PositiveBigIntegerField('ID do usuário', null=True, blank=True)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default=STATUS_STARTED, db_index=True)
    message = models.TextField('mensagem', blank=True)

    class Meta:
        verbose_name = 'evento Celery'
        verbose_name_plural = 'eventos Celery'
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['status', 'created_at'])]

    def __str__(self):
        return f'{self.task_name} - {self.get_status_display()}'
