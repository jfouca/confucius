from django import forms
from django.views.generic import ListView
from confucius.models import Account

class CreateAdminForm(forms.Form):
    title = forms.CharField(max_length=100)
    account = forms.ModelChoiceField(queryset = Account.objects.all())
