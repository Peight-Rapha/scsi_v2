from django import forms

from .models import InsuranceCompany


class InsuranceCompanyForm(forms.ModelForm):
    class Meta:
        model = InsuranceCompany
        fields = ('name', 'cnpj', 'contact_email', 'contact_phone')
