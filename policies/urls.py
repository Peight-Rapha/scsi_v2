from django.urls import path

from .views import GeneratePolicyView, PolicyCreateView, PolicyDeleteView, PolicyDetailView, PolicyListView, PolicyUpdateView


app_name = 'policies'

urlpatterns = [
    path('', PolicyListView.as_view(), name='list'),
    path('new/', PolicyCreateView.as_view(), name='create'),
    path('generate/<int:proposal_pk>/', GeneratePolicyView.as_view(), name='generate_from_proposal'),
    path('<int:pk>/', PolicyDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', PolicyUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', PolicyDeleteView.as_view(), name='delete'),
]
