"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from .views import health_check

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('', include('brokerages.urls')),
    path('accounts/', include('accounts.urls')),
    path('clients/', include('clients.urls')),
    path('insurers/', include('insurers.urls')),
    path('branches/', include('branches.urls')),
    path('covered-items/', include('covered_items.urls')),
    path('proposals/', include('proposals.urls')),
    path('policies/', include('policies.urls')),
    path('claims/', include('claims.urls')),
    path('attachments/', include('attachments.urls')),
    path('crm/', include('crm.urls')),
    path('renewals/', include('renewals.urls')),
    path('endorsements/', include('endorsements.urls')),
    path('commissions/', include('commissions.urls')),
    path('reports/', include('reports.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('ai/', include('ai_agents.urls')),
    path('notifications/', include('notifications.urls')),
    path('admin/', admin.site.urls),
]
