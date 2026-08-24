from django import forms

from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'document', 'email', 'phone', 'type', 'notes')
