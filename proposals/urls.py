from django.urls import path

from .views import CoverageDeleteView, ProposalCoverageCreateView, ProposalCoveredItemCreateView, ProposalCreateView, ProposalDeleteView, ProposalDetailView, ProposalListView, ProposalUpdateView


app_name = 'proposals'

urlpatterns = [
    path('', ProposalListView.as_view(), name='list'),
    path('new/', ProposalCreateView.as_view(), name='create'),
    path('<int:pk>/', ProposalDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ProposalUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ProposalDeleteView.as_view(), name='delete'),
    path('<int:proposal_pk>/items/new/', ProposalCoveredItemCreateView.as_view(), name='item_create'),
    path('<int:proposal_pk>/coverages/new/', ProposalCoverageCreateView.as_view(), name='coverage_create'),
    path('coverages/<int:pk>/delete/', CoverageDeleteView.as_view(), name='coverage_delete'),
]
