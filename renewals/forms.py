from django import forms

from base.models import BrokerageScopedFormMixin

from .models import Renewal


class RenewalForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('policy',)

    class Meta:
        model = Renewal
        fields = ('policy', 'due_date', 'status', 'notes')
