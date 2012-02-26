from django import forms
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm
from django.forms.models import inlineformset_factory

from confucius.models import Activation, Address, Email, Language, User


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email

    def save(self, commit=True):
        email = super(EmailForm, self).save(commit=False)

        if commit:
            email.save()
            if 'value' in self.changed_data:
                activation = Activation.objects.create(email=email)
                activation.send_email()

        return email


class UserCreationForm(AuthUserCreationForm):
    """
    Special form for User creation. Only mandatory fields plus
    the first_name (there's no meaning in typing the last_name alone).
    """
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30)

    class Meta(AuthUserCreationForm.Meta):
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        """
        Since we're subclassing the UserCreationForm from
        django.contrib.auth, we need to remove the field username
        because it holds no meaning inside confucius. It is just
        used as an underlying authentication token.
        """
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
        """
        Once the User created, we also need to create a main Email
        address belonging to him, and update its username since
        it's the only mandatory and unique field in the User model.
        The username is also necessary for the authentication backend.

        We can't use the email as is to fill the username field, because
        that field is only 30 characters long, and the email is absolutely
        not guaranteed to be that short. Instead, we use a special hashing
        function detailed in utils.py.
        """
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
        fields = ('first_name', 'languages', 'last_name')
        model = User
        ordering = ('first_name', 'last_name', 'languages')


class EmailFormSet(inlineformset_factory(User, Email)):
    extra = 1
    form = EmailForm
    has_main = False

    class Meta:
        model = Email
        exclude = ('user',)

    def clean(self):
        """
        This is where we check there's one and only one mail Email address.
        We can't do it in a Form object because emails (as ManyToMany) will
        always be updated as a batch. For that same reason, we can't enforce
        that constraint in the model either.
        """
        super(EmailFormSet, self).clean()

        try:
            for form in self.forms:
                if form.cleaned_data['main'] and not form.cleaned_data['DELETE']:
                    if self.has_main:
                        raise forms.ValidationError('There can only be one main %s.' % self.model.__name__)
                    self.has_main = True
        except:
            pass

        if not self.has_main:
            raise forms.ValidationError('There must be a main %s.' % self.model.__name__)


class AddressFormSet(inlineformset_factory(User, Address)):
    extra = 1

    class Meta:
        model = Email
        exclude = ('user',)
