from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


def private_upload_to(instance, filename):
    return f'private/brokerage_{instance.brokerage_id}/{filename}'


class Attachment(BrokerageModel):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='enviado por', on_delete=models.PROTECT, related_name='attachments')
    file = models.FileField('arquivo', upload_to=private_upload_to)
    original_name = models.CharField('nome original', max_length=255, blank=True)
    content_type = models.CharField('tipo de conteúdo', max_length=120, blank=True)
    size_bytes = models.PositiveBigIntegerField('tamanho em bytes', default=0)
    client = models.ForeignKey('clients.Client', verbose_name='cliente', on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    proposal = models.ForeignKey('proposals.Proposal', verbose_name='proposta', on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    policy = models.ForeignKey('policies.Policy', verbose_name='apólice', on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    claim = models.ForeignKey('claims.Claim', verbose_name='sinistro', on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)

    class Meta:
        verbose_name = 'anexo'
        verbose_name_plural = 'anexos'
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['brokerage', 'created_at'])]

    def __str__(self):
        return self.original_name or Path(self.file.name).name

    def clean(self):
        super().clean()
        links = [self.client, self.proposal, self.policy, self.claim]
        if not any(links):
            raise ValidationError('Informe ao menos um vínculo para o anexo.')
        for link in links:
            if link and link.brokerage_id != self.brokerage_id:
                raise ValidationError('O vínculo do anexo pertence a outra corretora.')

    def get_absolute_url(self):
        return reverse('attachments:download', kwargs={'pk': self.pk})
