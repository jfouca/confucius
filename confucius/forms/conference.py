from django import forms

from confucius.models import Alert, Conference


class AlertForm(forms.ModelForm):

    class Meta:
        model = Alert
        fields = ('reminder', 'event', 'trigger_date', 'action', 'title', 'content', 'roles')

    def __init__(self, *args, **kwargs):
        super(AlertForm, self).__init__(*args, **kwargs)
        self.fields['roles'].help_text = ''
        
    def clean(self):
        cleaned_data = super(AlertForm, self).clean()
        try:
            if cleaned_data['reminder'] is None and cleaned_data['event'] is None and cleaned_data['trigger_date'] is None and cleaned_data['action'] is None :
                raise forms.ValidationError('You must fill at least one of the following fields : Reminder, Action, Trigger date')
               
            if cleaned_data['reminder'] is not None and cleaned_data['event'] is None:
                raise forms.ValidationError('You must fill both of reminder and event fields')
                
            if cleaned_data['event'] is not None and cleaned_data['reminder'] is None:
                raise forms.ValidationError('You must fill both of reminder and event fields')
                
            if cleaned_data['action'] is not None and (cleaned_data['reminder'] is not None or cleaned_data['event'] is not None or cleaned_data['trigger_date'] is not None) :
                raise forms.ValidationError('One field only must be selected between Reminder, Trigger date and Action') 
                          
            if cleaned_data['trigger_date'] is not None and (cleaned_data['reminder'] is not None or cleaned_data['event'] is not None or cleaned_data['action'] is not None) :
                raise forms.ValidationError('One field only must be selected between Reminder, Trigger date and Action')  
                     
            if (cleaned_data['event'] is not None and cleaned_data['reminder'] is not None) and (cleaned_data['action'] is not None or cleaned_data['trigger_date'] is not None) :
                raise forms.ValidationError('One field only must be selected between Reminder, Trigger date and Action')
        except:
            pass

        return cleaned_data

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
