from django import forms

from confucius.forms import UserForm
from confucius.models import Alert, Conference, Domain, Email, Invitation, Membership, Role, User
from confucius.utils import email_to_username


class AlertForm(forms.ModelForm):

    class Meta:
        model = Alert
        exclude = ('conference')

    def clean(self):
        cleaned_data = super(AlertForm, self).clean()

        if cleaned_data['reminder'] is None and cleaned_data['event'] is None and cleaned_data['trigger_date'] is None and cleaned_data['action'] is None:
            raise forms.ValidationError('You must fill at least one of the following fields : Reminder, Action, Trigger date')

        if cleaned_data['reminder'] is not None and cleaned_data['event'] is None:
            raise forms.ValidationError('You must fill both of reminder and event fields')

        if cleaned_data['event'] is not None and cleaned_data['reminder'] is None:
            raise forms.ValidationError('You must fill both of reminder and event fields')

        if cleaned_data['action'] is not None and (cleaned_data['reminder'] is not None or cleaned_data['event'] is not None or cleaned_data['trigger_date'] is not None):
            raise forms.ValidationError('One field only must be selected between Reminder, Trigger date and Action')

        if cleaned_data['trigger_date'] is not None and (cleaned_data['reminder'] is not None or cleaned_data['event'] is not None or cleaned_data['action'] is not None):
            raise forms.ValidationError('One field only must be selected between Reminder, Trigger date and Action')

        if (cleaned_data['event'] is not None and cleaned_data['reminder'] is not None) and (cleaned_data['action'] is not None or cleaned_data['trigger_date'] is not None):
            raise forms.ValidationError('One field only must be selected between Reminder, Trigger date and Action')

        return cleaned_data


class ConferenceForm(forms.ModelForm):
    start_date = forms.DateField(label='Conference date')

    class Meta:
        model = Conference
        exclude = ('members', 'is_open', 'access_key', 'has_finalize_paper_selections', 'maximum_score',)

    def clean(self):
        cleaned_data = super(ConferenceForm, self).clean()
        start_date = cleaned_data['start_date']
        start_review = cleaned_data['reviews_start_date']
        end_review = cleaned_data['reviews_end_date']
        start_sub = cleaned_data['submissions_start_date']
        end_sub = cleaned_data['submissions_end_date']

        if end_sub < start_sub:
            raise forms.ValidationError('Submissions end date precedes Submissions start date in time')
        if start_review < end_sub:
            raise forms.ValidationError('Reviews start date precedes Submissions end date in time')
        if end_review < start_review:
            raise forms.ValidationError('Reviews end date precedes Reviews start date in time')
        if start_date < end_review:
            raise forms.ValidationError('Conference start date precedes Reviews end date in time')

        return cleaned_data


class InvitationForm(forms.Form):
    emails = forms.CharField(widget=forms.Textarea(), help_text='A whitespace-separated list of emails of people you wish to invite to the conference.', min_length=4)
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), widget=forms.CheckboxSelectMultiple(), help_text='What roles should the people above be given.')
    message = forms.CharField(widget=forms.Textarea(), label='Your personal message to each of them.', initial='Hello, ')

    def __init__(self, conference, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.conference = conference

    def clean(self):
        from hashlib import sha256
        from confucius.utils import random_string

        cleaned_data = super(InvitationForm, self).clean()

        if any(self.errors):
            return cleaned_data

        validator = forms.EmailField()
        values = set(cleaned_data['emails'].split())  # removing duplicates

        for value in values:  # every email is correct or we do nothing
            validator.clean(value)

        emails = Email.objects.filter(value__in=values)
        unregistered_values = values.difference(emails.values_list('value', flat=True))
        invitations = []

        for value in unregistered_values:
            user = User.objects.create(email=value, username=email_to_username(value), is_active=False)
            Email.objects.create(value=value, main=True, user=user)

        emails = Email.objects.filter(value__in=values)

        for email in emails:
            print "kikou",email.user
            try:
                invitation = Invitation.objects.create(user=email.user, conference=self.conference)
                invitation.key = sha256(random_string()).hexdigest()
                invitation.save()
                invitation.roles.add(*cleaned_data['roles'].all())
            except:
                invitation = Invitation.objects.get(user=email.user, conference=self.conference)

            invitations.append(invitation)

        return {'invitations': invitations, 'message': cleaned_data['message']}


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('domains',)
        widgets = {
            'domains': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(MembershipForm, self).__init__(*args, **kwargs)
        
        self.fields['domains'].help_text = "Your domains are linked to this conference only"
        self.fields['domains'].queryset = Domain.objects.filter(conferences__pk=self.instance.conference_id)


class SignupForm(UserForm):
    password1 = forms.CharField(label=u'Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'Password confirmation', widget=forms.PasswordInput)

    class Meta(UserForm.Meta):
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'languages')

    def __init__(self, email=True, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        if email:
            self.fields['email'].widget.attrs['readonly'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u"The two passwords didn't match.")
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        if 'readonly' in self.fields['email'].widget.attrs.keys() and self.fields['email'].widget.attrs['readonly'] == True:
            return email
        try:
            Email.objects.get(value=email)
        except Email.DoesNotExist:
            return email
        raise forms.ValidationError('This email is already taken.')

    def save(self, commit=True):
        user = super(SignupForm, self).save(False)
        
        if commit:
            user.set_password(self.cleaned_data.get('password1'))
            user.is_active = True
            user.username = email_to_username(user.email)
            user.save()
            user.languages = self.cleaned_data.get('languages')
            user.save()
            try:
                email = user.emails.get(main=True)
                email.confirmed = True
                email.save()
            except:
                pass

        return user


class SendEmailToUsersForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)
    users = forms.ModelMultipleChoiceField(queryset=None, required=False)

    roles = [[role.code, role.name] for role in Role.objects.all()]
    group = ["U", "Selected submitters"]
    choices = roles + [group]

    groups = forms.MultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(SendEmailToUsersForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = self.initial['conference'].members.all()

        roles = [[role.code, role.name] for role in Role.objects.all()]
        self.fields['groups'].choices = roles

        if self.initial['conference'].has_finalize_paper_selections == True:
            group_selected = ["U", "Selected submitters"]
            group_rejected = ["X", "Rejected submitters"]
            choices = [group_selected] + [group_rejected] + roles
            self.fields['groups'].choices = choices

    def clean(self):
        cleaned_data = super(SendEmailToUsersForm, self).clean()

        if len(cleaned_data['users']) == 0 and len(cleaned_data['groups']) == 0:
            raise forms.ValidationError('You must fill at least one of the following fields : Receivers, Groups')

        return cleaned_data
