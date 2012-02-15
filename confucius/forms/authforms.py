from django import forms

from confucius.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
