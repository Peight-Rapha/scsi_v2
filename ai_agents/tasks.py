from celery import shared_task

from brokerages.models import Brokerage
from dj_celery_panel.models import CeleryTaskEvent
from notifications.models import Notification

from .services import build_summary
from .tools import get_entity_for_brokerage


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 2}, time_limit=300)
def summarize_entity(self, brokerage_id, user_id, entity_type, entity_id):
    brokerage = Brokerage.objects.get(pk=brokerage_id)
    event = CeleryTaskEvent.objects.create(task_name='summarize_entity', task_id=self.request.id or '', brokerage_id=brokerage_id, user_id=user_id)
    try:
        entity = get_entity_for_brokerage(entity_type, entity_id, brokerage)
        entity.ai_summary = build_summary(entity_type, entity)
        entity.save(update_fields=['ai_summary', 'updated_at'])
        Notification.objects.create(brokerage=brokerage, user_id=user_id, title='Resumo com IA pronto', message=f'O resumo de {entity} foi atualizado.', level=Notification.LEVEL_SUCCESS)
        event.status = CeleryTaskEvent.STATUS_SUCCESS
        event.message = f'Resumo atualizado para {entity_type} #{entity_id}.'
        event.save(update_fields=['status', 'message', 'updated_at'])
    except Exception as exc:
        Notification.objects.create(brokerage=brokerage, user_id=user_id, title='Falha no resumo com IA', message='Não foi possível concluir a análise. Tente novamente mais tarde.', level=Notification.LEVEL_ERROR)
        event.status = CeleryTaskEvent.STATUS_FAILURE
        event.message = str(exc)[:1000]
        event.save(update_fields=['status', 'message', 'updated_at'])
        raise exc
