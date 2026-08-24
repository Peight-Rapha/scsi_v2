from django import forms

from base.models import BrokerageScopedFormMixin

from .models import Endorsement


class EndorsementForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('policy',)

    class Meta:
        model = Endorsement
        fields = ('policy', 'endorsement_number', 'type', 'description', 'effective_date')
