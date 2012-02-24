from django import forms

from confucius.models import Alert, Conference


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ('reminder', 'event', 'trigger_date', 'action', 'title', 'content', 'for_president', 'roles')

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
    
    def __init__(self, *args, **kwargs):
        super(DomainsForm, self).__init__(*args, **kwargs)
        self.fields['domains'].help_text = ''
    
    class Meta:
        model = Conference
        exclude = ('title','accounts','president','help_text','startConfDate','startConfDate','endConfDate',
        'startSubmitDate','endSubmitDate','startEvaluationDate','endEvaluationDate','url','isOpen')
        widgets = {	    
	    'domains' : forms.CheckboxSelectMultiple()
	    }
