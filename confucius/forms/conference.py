from django import forms

from confucius.models import Alert, Conference


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ('reminder', 'event', 'trigger_date', 'action', 'title', 'content', 'roles')

    def __init__(self, *args, **kwargs):
        super(AlertForm, self).__init__(*args, **kwargs)
        self.fields['roles'].help_text = ''


class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        exclude = ('members', 'is_open')
        
        
class InvitationForm(forms.Form):
    email = forms.EmailField()
    invitation_text = forms.CharField(widget=forms.Textarea)


class DomainsForm(forms.ModelForm):
    domains = forms.ModelMultipleChoiceField(Domain.objects.all(), required=True)
    
    def __init__(self, *args, **kwargs):
        pk_conference = kwargs.pop('pk_conference')
        super(InvitationForm, self).__init__(*args, **kwargs)
        # Building domains, from an existing paper and a conference's id
        self.fields["domains"].queryset = Conference.objects.get(pk=pk_conference).domains
