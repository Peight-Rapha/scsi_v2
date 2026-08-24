from django import forms

from .models import InsuranceBranch


class InsuranceBranchForm(forms.ModelForm):
    class Meta:
        model = InsuranceBranch
        fields = ('name', 'description')
