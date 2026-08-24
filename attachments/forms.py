from django import forms

from base.models import BrokerageScopedFormMixin

from .models import Attachment


class AttachmentForm(BrokerageScopedFormMixin, forms.ModelForm):
    brokerage_scoped_fields = ('client', 'proposal', 'policy', 'claim')

    class Meta:
        model = Attachment
        fields = ('file', 'client', 'proposal', 'policy', 'claim')
