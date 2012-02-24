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

        super(AlertForm, self).clean()

        try:
            if self.cleaned_data['reminder'] is None and self.cleaned_data['event'] is None and self.cleaned_data['trigger_date'] is None and self.cleaned_data['action'] is None :
               raise forms.ValidationError('You must fill at least one of the following fields : Reminder, Action, Trigger date')
            if self.cleaned_data['reminder'] is not None and self.cleaned_data['event'] is None:
                raise forms.ValidationError('You must fill both of reminder and event fields')
            if self.cleaned_data['event'] is not None and self.cleaned_data['reminder'] is None:
                raise forms.ValidationError('You must fill both of reminder and event fields')
            if self.cleaned_data['action'] is not None :
                if self.cleaned_data['reminder'] is not None or self.cleaned_data['event'] is not None or self.cleaned_data['trigger_date'] is not None:
                    raise forms.ValidationError('One field only must be selected between Reminder, Trigger date and Action')       
            if self.cleaned_data['trigger_date'] is not None :
                if self.cleaned_data['reminder'] is not None or self.cleaned_data['event'] is not None or self.cleaned_data['action'] is not None:
                    raise forms.ValidationError('One field only must be selected between Reminder, Trigger date and Action')   
            if self.cleaned_data['event'] is not None and self.cleaned_data['reminder'] is not None:
                if self.cleaned_data['action'] is not None or self.cleaned_data['trigger_date'] is not None :
                    raise forms.ValidationError('One field only must be selected between Reminder, Trigger date and Action')          
        except KeyError:
            pass



class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        exclude = ('members', 'is_open')
