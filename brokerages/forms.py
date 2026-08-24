from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction

from .models import Brokerage


class SignupForm(forms.Form):
    first_name = forms.CharField(label='Nome', max_length=150)
    last_name = forms.CharField(label='Sobrenome', max_length=150, required=False)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    cnpj = forms.CharField(label='CNPJ', max_length=18)
    legal_name = forms.CharField(label='Razão social', max_length=200)
    name = forms.CharField(label='Nome fantasia', max_length=150, required=False)
    plan = forms.ChoiceField(label='Plano', choices=Brokerage.PLAN_CHOICES, initial=Brokerage.PLAN_FREE)

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe usuário com este email.')
        return email

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        if Brokerage.objects.filter(cnpj=cnpj).exists():
            raise forms.ValidationError('Já existe corretora com este CNPJ.')
        return cnpj

    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        brokerage = Brokerage.objects.create(
            name=data.get('name') or data['legal_name'],
            legal_name=data['legal_name'],
            cnpj=data['cnpj'],
            plan=Brokerage.PLAN_FREE,
        )
        user = get_user_model().objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data.get('last_name', ''),
            brokerage=brokerage,
        )
        group, _ = Group.objects.get_or_create(name='brokerage_owner')
        user.groups.add(group)
        return user
