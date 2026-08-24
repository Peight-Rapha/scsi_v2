from django.urls import path

from .views import signup


app_name = 'brokerages'

urlpatterns = [
    path('signup/', signup, name='signup'),
]
