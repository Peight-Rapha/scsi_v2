from django import forms

from base.models import BrokerageScopedFormMixin

from .models import Claim


class ClaimForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('client', 'policy', 'covered_item')

    class Meta:
        model = Claim
        fields = ('client', 'policy', 'covered_item', 'claim_number', 'status', 'occurred_at', 'description')
