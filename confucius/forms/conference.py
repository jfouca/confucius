from django import forms

from confucius.forms import UserForm
from confucius.models import Alert, Conference, Domain, Email, Invitation, Membership, User
from datetime import datetime


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
        exclude = ('members', 'is_open', 'access_key', 'has_finalize_paper_selections', 'maximum_score')

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


class InvitationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Invitation
        fields = ('email', 'roles', 'message')
        widgets = {
            'roles': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.fields['roles'].help_text = ""
        self.fields['message'].label = "Additional message"

    def clean(self):
        from hashlib import sha256
        from confucius.utils import email_to_username, random_string

        cleaned_data = super(InvitationForm, self).clean()

        if any(self.errors):
            return cleaned_data

        email = None
        membership = None

        try:
            email = Email.objects.get(value=cleaned_data['email'])
            membership = Membership.objects.get(user=email.user, conference=cleaned_data['conference'], roles__in=cleaned_data['roles'])
        except:
            pass

        if membership is not None:
            raise forms.ValidationError(u'This user has already that role in the Conference.')

        if email is None:
            user = User.objects.create(email=cleaned_data['email'], username=email_to_username(cleaned_data['email']), is_active=False)
            Email.objects.create(value=user.email, main=True, user=user)
        else:
            user = email.user

        self.instance.user = user
        self.instance.key = sha256(random_string()).hexdigest()

        try:
            self.instance.validate_unique()
        except forms.ValidationError:
            raise forms.ValidationError(u'This user has already been invited to the conference.')

        return cleaned_data

    def save(self, request, template_name='conference/invitation_email.html'):
        from django.contrib.sites.models import get_current_site
        from django.core.mail import send_mail
        from django.template import Context, loader

        invitation = super(InvitationForm, self).save(commit=False)
        template = loader.get_template(template_name)
        context = {
            'domain': get_current_site(request).domain,
            'invitation': invitation,
            'roles': self.cleaned_data['roles']  # We can't use invitation.roles in the template since the invitation has not been persisted yet
        }

        send_mail('You have been invited to participate in the conference "%s"' % invitation.conference,
            template.render(Context(context)), None, [invitation.user.email])

        invitation.save()
        self.save_m2m()

        return invitation


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

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['readonly'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u"The two passwords didn't match.")
        return password2

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit)

        if commit:
            user.set_password(self.cleaned_data.get('password1'))
            user.is_active = True
            user.save()
            email = user.emails.get(main=True)
            email.confirmed = True
            email.save()

        return user


class SendEmailToUsersForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)
    receivers = forms.ModelMultipleChoiceField(queryset=None, required=True)

    def __init__(self, *args, **kwargs):
        super(SendEmailToUsersForm, self).__init__(*args, **kwargs)
        self.fields['receivers'].queryset = self.initial['conference'].members.all()
