from django import forms
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm
from django.contrib.auth.models import User
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from confucius.models import Address, Email, Language


class UserCreationForm(AuthUserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30)

    class Meta(AuthUserCreationForm.Meta):
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        del self.base_fields['username']
        del self.fields['username']

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Email.objects.get(value=email)
        except Email.DoesNotExist:
            return email
        raise forms.ValidationError('This email is already taken.')

    def save(self, **kwargs):
        from confucius.utils import email_to_username

        user = super(UserCreationForm, self).save(commit=False)
        user.username = email_to_username(user.email)
        user.save()
        Email.objects.create(value=user.email, main=True, user=user)

        return user


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all(), required=False)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('first_name', 'languages', 'last_name')


class EmailFormSet(inlineformset_factory(User, Email)):
    extra = 1
    has_main = False

    def clean(self):
        super(EmailFormSet, self).clean()

        try:
            for form in self.forms:
                if form.cleaned_data['main'] and not form.cleaned_data['DELETE']:
                    if self.has_main:
                        raise forms.ValidationError('There can only be one main %s.' % self.model.__name__)
                    self.has_main = True
        except KeyError:
            pass

        if not self.has_main:
            raise forms.ValidationError('There must be a main %s.' % self.model.__name__)


class AddressFormSet(inlineformset_factory(User, Address)):
    extra = 1
