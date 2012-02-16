from django import forms

from confucius.models import Account
from confucius.widgets import ForeignKeySearchInput


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        widgets = {
            'languages': ForeignKeySearchInput(),
        }
