from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import ModelForm, Form
from confucius.models import Account, Role, Conference, Alert
from django.contrib.admin import widgets 
from django.contrib.admin.widgets import AdminDateWidget 

class AlertForm(ModelForm): 

    class Meta:
        model = Alert
        fields=('reminder','event','trigger_date','action','title','content','forPresident','roles')

    def __init__(self, *args, **kwargs):
        super(AlertForm, self).__init__(*args, **kwargs)
        self.fields['roles'].help_text = ''

