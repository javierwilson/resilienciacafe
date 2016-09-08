# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from django_countries import countries

from forocacao.app.models import Event, Profession

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First name'))
    last_name = forms.CharField(max_length=30, label=_('Last name'))
    SEX_CHOICES = (('M',_('Male')), ('F', _('Female')))
    sex = forms.ChoiceField(choices=SEX_CHOICES, label=_('Gender'))
    organization = forms.CharField(max_length=30, label=_('Organization'))
    position = forms.CharField(max_length=30, label=_('Job title'), required=True)
    country = forms.ChoiceField(countries, label=_('Country'))
    emergency_name = forms.CharField(max_length=30, label=_('Emergency Contact Name'))
    emergency_phone = forms.CharField(max_length=30, label=_('Emergency Contact Telephone'))
    extra = forms.BooleanField(required=False, label=_('I am  interested in participating in the field visit 22 and 23rd of September'))
    translation = forms.BooleanField(required=False, label=_('The forum will be held in Spanish.  Will you need translation to English?'))
    text = forms.CharField(required=False, widget=forms.Textarea, label=_('What is your experience with coffee and resilience?'))

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus'})
        self.keyOrder = ['firs_name', 'last_name', 'country', 'document', 'phone', 'email', 'password']

    def signup(self, request, user):
        user.username = self.cleaned_data['email'][:30]
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.organization = self.cleaned_data['organization']
        user.position = self.cleaned_data['position']
        user.emergency_name = self.cleaned_data['emergency_name']
        user.emergency_phone = self.cleaned_data['emergency_phone']
        user.country = self.cleaned_data['country']
        user.sex = self.cleaned_data['sex']
        user.extra = self.cleaned_data['extra']
        user.text = self.cleaned_data['text']
        user.translation = self.cleaned_data['translation']
        event = Event.objects.filter(status='frontpage')[0]
        if event:
            user.event = event
        user.save()
