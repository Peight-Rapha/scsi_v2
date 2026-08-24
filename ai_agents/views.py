from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, TemplateView

from base.models import TenantObjectMixin, TenantQuerySetMixin, get_tenant_object_or_404
from base.views import InternalViewMixin

from .models import AIChatMessage, AIChatSession
from .services import answer_chat
from .tasks import summarize_entity


class SummarizeEntityView(InternalViewMixin, View):
    def post(self, request, entity_type, pk):
        summarize_entity.delay(request.brokerage.pk, request.user.pk, entity_type, pk)
        return redirect(request.POST.get('next') or 'dashboard:index')


class ChatView(InternalViewMixin, TemplateView):
    template_name = 'ai_agents/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessions'] = AIChatSession.objects.for_brokerage(self.request.brokerage).filter(user=self.request.user)
        return context

    def post(self, request):
        title = request.POST.get('title') or 'Nova conversa'
        session = AIChatSession.objects.create(brokerage=request.brokerage, user=request.user, title=title)
        return redirect(session.get_absolute_url())


class ChatSessionView(InternalViewMixin, TenantQuerySetMixin, DetailView):
    model = AIChatSession
    template_name = 'ai_agents/chat_session.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).prefetch_related('messages')

    def post(self, request, pk):
        session = get_tenant_object_or_404(AIChatSession, request.brokerage, pk=pk, user=request.user)
        question = request.POST.get('message', '').strip()
        if question:
            AIChatMessage.objects.create(brokerage=request.brokerage, session=session, role=AIChatMessage.ROLE_USER, content_markdown=question)
            answer = answer_chat(request.brokerage, question)
            AIChatMessage.objects.create(brokerage=request.brokerage, session=session, role=AIChatMessage.ROLE_ASSISTANT, content_markdown=answer)
            session.save(update_fields=['updated_at'])
        return redirect(session.get_absolute_url())
