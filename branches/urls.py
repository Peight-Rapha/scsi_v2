from django.urls import path

from .views import InsuranceBranchCreateView, InsuranceBranchDeleteView, InsuranceBranchDetailView, InsuranceBranchListView, InsuranceBranchUpdateView


app_name = 'branches'

urlpatterns = [
    path('', InsuranceBranchListView.as_view(), name='list'),
    path('new/', InsuranceBranchCreateView.as_view(), name='create'),
    path('<int:pk>/', InsuranceBranchDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', InsuranceBranchUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', InsuranceBranchDeleteView.as_view(), name='delete'),
]
