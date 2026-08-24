from django.urls import path

from .views import DealCreateView, DealDeleteView, DealDetailView, DealKanbanView, DealListView, DealStageCreateView, DealStageUpdateView, DealUpdateView, MoveDealStageView


app_name = 'crm'

urlpatterns = [
    path('', DealListView.as_view(), name='list'),
    path('kanban/', DealKanbanView.as_view(), name='kanban'),
    path('new/', DealCreateView.as_view(), name='create'),
    path('stages/new/', DealStageCreateView.as_view(), name='stage_create'),
    path('stages/<int:pk>/edit/', DealStageUpdateView.as_view(), name='stage_update'),
    path('<int:pk>/', DealDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', DealUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', DealDeleteView.as_view(), name='delete'),
    path('<int:pk>/move/', MoveDealStageView.as_view(), name='move'),
]
