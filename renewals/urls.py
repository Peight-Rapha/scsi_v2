from django.urls import path

from .views import RenewalCreateView, RenewalDeleteView, RenewalDetailView, RenewalListView, RenewalUpdateView


app_name = 'renewals'

urlpatterns = [
    path('', RenewalListView.as_view(), name='list'),
    path('new/', RenewalCreateView.as_view(), name='create'),
    path('<int:pk>/', RenewalDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', RenewalUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', RenewalDeleteView.as_view(), name='delete'),
]
