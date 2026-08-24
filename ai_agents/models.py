from django.conf import settings
from django.db import models
from django.urls import reverse

from base.models import BrokerageModel


class AIChatSession(BrokerageModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário', on_delete=models.CASCADE, related_name='ai_chat_sessions')
    title = models.CharField('título', max_length=180, default='Nova conversa')

    class Meta:
        verbose_name = 'sessão de chat IA'
        verbose_name_plural = 'sessões de chat IA'
        ordering = ('-updated_at',)
        indexes = [models.Index(fields=['brokerage', 'user', 'updated_at'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ai_agents:chat_session', kwargs={'pk': self.pk})


class AIChatMessage(BrokerageModel):
    ROLE_USER = 'user'
    ROLE_ASSISTANT = 'assistant'
    ROLE_CHOICES = ((ROLE_USER, 'Usuário'), (ROLE_ASSISTANT, 'Assistente'))

    session = models.ForeignKey(AIChatSession, verbose_name='sessão', on_delete=models.CASCADE, related_name='messages')
    role = models.CharField('papel', max_length=20, choices=ROLE_CHOICES)
    content_markdown = models.TextField('conteúdo em Markdown')

    class Meta:
        verbose_name = 'mensagem de chat IA'
        verbose_name_plural = 'mensagens de chat IA'
        ordering = ('created_at',)
        indexes = [models.Index(fields=['brokerage', 'session', 'created_at'])]

    def __str__(self):
        return f'{self.get_role_display()}: {self.content_markdown[:40]}'

    @property
    def content_html(self):
        return render_markdown(self.content_markdown)


def render_markdown(content):
    try:
        import bleach
        import markdown
    except ImportError:
        return content.replace('\n', '<br>')
    html = markdown.markdown(content, extensions=['extra'])
    return bleach.clean(html, tags=['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'code', 'pre', 'blockquote', 'h1', 'h2', 'h3'], attributes={}, strip=True)
