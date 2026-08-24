from django.urls import path

from .views import AgentCreateView, AgentDetailView, AgentListView, AgentUpdateView, CommissionCreateView, CommissionDeleteView, CommissionDetailView, CommissionListView, CommissionUpdateView, ProducerCreateView, ProducerDetailView, ProducerListView, ProducerUpdateView

app_name = 'commissions'

urlpatterns = [
    path('', CommissionListView.as_view(), name='list'),
    path('new/', CommissionCreateView.as_view(), name='create'),
    path('<int:pk>/', CommissionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', CommissionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', CommissionDeleteView.as_view(), name='delete'),
    path('agents/', AgentListView.as_view(), name='agents'),
    path('agents/new/', AgentCreateView.as_view(), name='agent_create'),
    path('agents/<int:pk>/', AgentDetailView.as_view(), name='agent_detail'),
    path('agents/<int:pk>/edit/', AgentUpdateView.as_view(), name='agent_update'),
    path('producers/', ProducerListView.as_view(), name='producers'),
    path('producers/new/', ProducerCreateView.as_view(), name='producer_create'),
    path('producers/<int:pk>/', ProducerDetailView.as_view(), name='producer_detail'),
    path('producers/<int:pk>/edit/', ProducerUpdateView.as_view(), name='producer_update'),
]
