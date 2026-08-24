from django import forms
from django.contrib.auth import get_user_model

from base.models import BrokerageScopedFormMixin

from .models import Deal, DealStage


class DealStageForm(forms.ModelForm):
    class Meta:
        model = DealStage
        fields = ('name', 'color', 'position')


class DealForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('client', 'stage')

    class Meta:
        model = Deal
        fields = ('client', 'stage', 'title', 'estimated_value', 'status', 'assigned_to')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.brokerage and 'assigned_to' in self.fields:
            self.fields['assigned_to'].queryset = get_user_model().objects.filter(brokerage=self.brokerage)
