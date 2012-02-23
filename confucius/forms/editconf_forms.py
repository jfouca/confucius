from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import ModelForm
from confucius.models import Account, ConferenceAccountRole, Conference
from django.contrib.admin import widgets 
from django.contrib.admin.widgets import AdminDateWidget 

class EditConfForm(ModelForm): 

    

    def __init__(self, *args, **kwargs):
        super(EditConfForm, self).__init__(*args, **kwargs)
	self.fields['domains'].help_text = ''
	self.fields['isOpen'].label = 'Open'
        self.fields['startConfDate'].label = 'Conference starting date'
        self.fields['endConfDate'].label = 'Conference ending date'
        self.fields['startSubmitDate'].label = 'Submission starting date'
        self.fields['endSubmitDate'].label = 'Submission ending date'
        self.fields['startEvaluationDate'].label = 'Evaluation starting date'
        self.fields['endEvaluationDate'].label = 'Evaluation ending date'
        self.fields['url'].label = 'Homepage'

    class Meta:
        model = Conference
        exclude = ('title','accounts','president','help_text')
        widgets = {
	    'startConfDate': AdminDateWidget(),
	    'endConfDate': AdminDateWidget(),
	    'startSubmitDate': AdminDateWidget(),
	    'endSubmitDate': AdminDateWidget(),
	    'startEvaluationDate': AdminDateWidget(),
	    'endEvaluationDate': AdminDateWidget(),	    
	    'domains' : forms.CheckboxSelectMultiple()
	}

	
class InviteReviewerForm(forms.Form):
    email = forms.EmailField()


class DomainsForm(ModelForm):
    
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

