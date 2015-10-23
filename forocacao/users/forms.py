# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from forocacao.app.models import Event

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First name'))
    last_name = forms.CharField(max_length=30, label=_('Last name'))
    document = forms.CharField(max_length=30, label=_('Document ID'))
    phone = forms.CharField(max_length=30, label=_('Telephone'))
    organization = forms.CharField(max_length=30, label=_('Organization'))
    position = forms.CharField(max_length=30, label=_('Position'))

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus'})
        self.keyOrder = ['firs_name', 'last_name', 'document', 'phone', 'email', 'password']

    def signup(self, request, user):
        user.username = self.cleaned_data['email'][:30]
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        event = Event.objects.filter(status='frontpage')[0]
        if event:
            user.event = event
        user.save()
