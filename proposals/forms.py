from django import forms

from base.models import BrokerageScopedFormMixin

from .models import Coverage, Proposal


class ProposalForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('client', 'insurance_company', 'branch')

    class Meta:
        model = Proposal
        fields = ('client', 'insurance_company', 'branch', 'status', 'premium_amount', 'commission_rate', 'valid_until')


class CoverageForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('proposal',)

    class Meta:
        model = Coverage
        fields = ('proposal', 'policy_id', 'name', 'limit_amount', 'deductible_amount')
