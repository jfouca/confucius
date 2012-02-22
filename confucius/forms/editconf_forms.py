from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import ModelForm
from confucius.models import Account, ConferenceAccountRole, Conference
from django.contrib.admin import widgets 
from django.contrib.admin.widgets import AdminDateWidget 

class EditConfForm(ModelForm): 
    def __init__(self, *args, **kwargs):
        super(EditConfForm, self).__init__(*args, **kwargs)
        self.fields['startConfDate'].label = 'Conference starting date'
        self.fields['endConfDate'].label = 'Conference ending date'
        self.fields['startSubmitDate'].label = 'Submission starting date'
        self.fields['endSubmitDate'].label = 'Submission ending date'
        self.fields['startEvaluationDate'].label = 'Evaluation starting date'
        self.fields['endEvaluationDate'].label = 'Evaluation ending date'
        self.fields['url'].label = 'Homepage'

    class Meta:
        model = Conference
        exclude = ('title','accounts','president','help_text', 'isOpen', 'domains')