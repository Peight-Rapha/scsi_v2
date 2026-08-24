from django.urls import path

from .views import EndorsementCreateView, EndorsementDeleteView, EndorsementDetailView, EndorsementListView, EndorsementUpdateView

app_name = 'endorsements'

urlpatterns = [
    path('', EndorsementListView.as_view(), name='list'),
    path('new/', EndorsementCreateView.as_view(), name='create'),
    path('<int:pk>/', EndorsementDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', EndorsementUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', EndorsementDeleteView.as_view(), name='delete'),
]
