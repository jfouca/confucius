from django import forms

from confucius.models import Alert, Conference, Domain


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
    
    class Meta:
        model = Conference
        exclude = ('members', 'is_open','has_finalize_paper_selections','title',
        'start_date','submissions_start_date','submissions_end_date','reviews_start_date',
        'reviews_end_date','url')
    
    def __init__(self, *args, **kwargs):
        conference = kwargs.pop('instance', None)
        super(DomainsForm, self).__init__(*args, **kwargs)
        # Building domains, from an existing paper and a conference's id
        self.fields["domains"].queryset = Conference.objects.get(pk=conference.id).domains
        self.fields["domains"].initial = conference.domains.all()    
