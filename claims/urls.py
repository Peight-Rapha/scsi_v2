from django.urls import path

from .views import ClaimCreateView, ClaimDeleteView, ClaimDetailView, ClaimListView, ClaimUpdateView


app_name = 'claims'

urlpatterns = [
    path('', ClaimListView.as_view(), name='list'),
    path('new/', ClaimCreateView.as_view(), name='create'),
    path('<int:pk>/', ClaimDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ClaimUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ClaimDeleteView.as_view(), name='delete'),
]
