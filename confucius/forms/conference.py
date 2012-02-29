from django import forms

from confucius.models import Alert, Conference, Domain, Email, Invitation, Membership, User


class AlertForm(forms.ModelForm):
    conference = forms.ModelChoiceField(queryset=Conference.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Alert

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
    class Meta:
        model = Conference
        exclude = ('members', 'is_open')


class InvitationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Invitation
        fields = ('email', 'roles', 'message')
        widgets = {
            'roles': forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        from hashlib import sha256
        from confucius.utils import email_to_username, random_string

        cleaned_data = super(InvitationForm, self).clean()
        email = None
        membership = None

        try:
            email = Email.objects.get(value=cleaned_data['email'])
            membership = Membership.objects.get(user=email.user, conference=cleaned_data['conference'], roles__in=(cleaned_data['role'],))
        except:
            pass

        if membership is not None:
            raise forms.ValidationError(u'This user has already that role in the Conference.')

        if email is None:
            user = User.objects.create(email=self.cleaned_data['email'], username=email_to_username(self.cleaned_data['email']))
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

        self.fields['domains'].queryset = Domain.objects.filter(conferences__pk=self.instance.conference_id)
        
class SendEmailToUsersForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True, widget = forms.Textarea)
    receivers = forms.ModelMultipleChoiceField(queryset=None, required=True)
    
    def __init__(self, *args, **kwargs):
        super(SendEmailToUsersForm, self).__init__(*args, **kwargs)
        self.fields['receivers'].queryset = self.initial['conference'].members.all()  
