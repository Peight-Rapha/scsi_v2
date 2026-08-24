from django.urls import path

from .views import ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, ClientUpdateView


app_name = 'clients'

urlpatterns = [
    path('', ClientListView.as_view(), name='list'),
    path('new/', ClientCreateView.as_view(), name='create'),
    path('<int:pk>/', ClientDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ClientUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='delete'),
]
