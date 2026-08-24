from django.urls import path

from .views import InsuranceCompanyCreateView, InsuranceCompanyDeleteView, InsuranceCompanyDetailView, InsuranceCompanyListView, InsuranceCompanyUpdateView


app_name = 'insurers'

urlpatterns = [
    path('', InsuranceCompanyListView.as_view(), name='list'),
    path('new/', InsuranceCompanyCreateView.as_view(), name='create'),
    path('<int:pk>/', InsuranceCompanyDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', InsuranceCompanyUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', InsuranceCompanyDeleteView.as_view(), name='delete'),
]
