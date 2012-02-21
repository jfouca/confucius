from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import ugettext, ugettext_lazy as _

from confucius.models import Account, Language, ConferenceAccountRole


class AdminAccountForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30)
    is_active = forms.BooleanField(required=False)

    class Meta:
        model = Account

    def __init__(self, *args, **kwargs):
        super(AdminAccountForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['is_active'].initial = self.instance.is_active
        except Exception:
            pass

    def save(self, *args, **kwargs):
        if self.instance.pk == None:
            self.instance = Account.objects.create(self.cleaned_data[''], "kikou", self.cleaned_data['last_name'])

        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.user.is_active = self.cleaned_data['is_active']
        self.instance.user.save()
        return super(AdminAccountForm, self).save(*args, **kwargs)


class ConferenceAccountRoleForm(forms.ModelForm):
    class Meta:
        model = ConferenceAccountRole
        widgets = {
            'role': CheckboxSelectMultiple(),
        }
        
class CreateAccountForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password_1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password_2 = forms.CharField(label=_("Password confirmation	"), widget=forms.PasswordInput, help_text = _("Enter the same password as above, for verification."))
    language = forms.ModelChoiceField(label=_("Native Language"), queryset = Language.objects.all())
    error_messages = {
        'duplicate_username': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
