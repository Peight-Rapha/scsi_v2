from django.urls import path

from .views import CoveredItemCreateView, CoveredItemDeleteView, CoveredItemDetailView, CoveredItemListView, CoveredItemUpdateView


app_name = 'covered_items'

urlpatterns = [
    path('', CoveredItemListView.as_view(), name='list'),
    path('new/', CoveredItemCreateView.as_view(), name='create'),
    path('<int:pk>/', CoveredItemDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', CoveredItemUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', CoveredItemDeleteView.as_view(), name='delete'),
]
