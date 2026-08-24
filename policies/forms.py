from django import forms

from base.models import BrokerageScopedFormMixin

from .models import Policy


class PolicyForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('proposal', 'client', 'insurance_company', 'branch')

    class Meta:
        model = Policy
        fields = ('proposal', 'client', 'insurance_company', 'branch', 'policy_number', 'start_date', 'end_date', 'premium_amount', 'status')
