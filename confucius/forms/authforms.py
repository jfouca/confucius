from django import forms

from confucius.models import Profile
from confucius.widgets import ForeignKeySearchInput


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'languages': ForeignKeySearchInput(),
        }
