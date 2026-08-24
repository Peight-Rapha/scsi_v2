from django import forms

from base.models import BrokerageScopedFormMixin

from .models import CoveredItem


class CoveredItemForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('proposal',)

    class Meta:
        model = CoveredItem
        fields = ('proposal', 'policy_id', 'item_type', 'description', 'insured_value', 'metadata')
