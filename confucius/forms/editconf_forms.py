from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from confucius.models import Conference


class EditConfForm(forms.ModelForm):
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
        widgets = {
            'startConfDate': AdminDateWidget(),
            'endConfDate': AdminDateWidget(),
            'startSubmitDate': AdminDateWidget(),
            'endSubmitDate': AdminDateWidget(),
            'startEvaluationDate': AdminDateWidget(),
            'endEvaluationDate': AdminDateWidget(),
            'domains': forms.CheckboxSelectMultiple()
        }
        exclude = ('title', 'accounts', 'president', 'help_text', 'isOpen', 'domains')
