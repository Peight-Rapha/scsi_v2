from django.urls import path

from .views import AttachmentCreateView, AttachmentDeleteView, AttachmentDownloadView, AttachmentListView


app_name = 'attachments'

urlpatterns = [
    path('', AttachmentListView.as_view(), name='list'),
    path('new/', AttachmentCreateView.as_view(), name='create'),
    path('<int:pk>/download/', AttachmentDownloadView.as_view(), name='download'),
    path('<int:pk>/delete/', AttachmentDeleteView.as_view(), name='delete'),
]
