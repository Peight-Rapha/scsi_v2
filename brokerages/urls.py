from django.urls import path

from .views import landing, signup


app_name = 'brokerages'

urlpatterns = [
    path('', landing, name='landing'),
    path('signup/', signup, name='signup'),
]
