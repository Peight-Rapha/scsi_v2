from django import forms

from base.models import BrokerageScopedFormMixin

from .models import Agent, Commission, Producer


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('name', 'document', 'type', 'commission_rate')


class ProducerForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('agent',)

    class Meta:
        model = Producer
        fields = ('agent', 'name', 'document', 'commission_rate')


class CommissionForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('policy', 'agent', 'producer')

    class Meta:
        model = Commission
        fields = ('policy', 'agent', 'producer', 'gross_amount', 'status')
