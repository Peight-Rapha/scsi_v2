from django.urls import path

from .views import ChatSessionView, ChatView, SummarizeEntityView

app_name = 'ai_agents'

urlpatterns = [
    path('summarize/<slug:entity_type>/<int:pk>/', SummarizeEntityView.as_view(), name='summarize'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('chat/<int:pk>/', ChatSessionView.as_view(), name='chat_session'),
]
