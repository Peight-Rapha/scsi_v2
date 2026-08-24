from django.urls import path

from .views import ReportCSVView, ReportPDFView, ReportsIndexView

app_name = 'reports'

urlpatterns = [
    path('', ReportsIndexView.as_view(), name='index'),
    path('<slug:slug>.csv', ReportCSVView.as_view(), name='csv'),
    path('<slug:slug>.pdf', ReportPDFView.as_view(), name='pdf'),
    path('commissions.csv', ReportCSVView.as_view(), {'slug': 'commissions'}, name='commissions_csv'),
]
