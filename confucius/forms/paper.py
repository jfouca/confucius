from django import forms
from confucius.models import Domain, Membership, Paper, Role


class PaperForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'description', 'file', 'co_authors', 'language', 'domains')
        model = Paper
        widgets = {
            'domains': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(PaperForm, self).__init__(*args, **kwargs)

        self.fields['domains'].queryset = Domain.objects.filter(conferences__pk=self.instance.conference_id)

    def save(self, commit=True):
        paper = super(PaperForm, self).save(commit)

        membership, created = Membership.objects.get_or_create(user=paper.submitter, conference=paper.conference)
        membership.roles.add(Role.objects.get(code='S'))
        membership.set_last_accessed()

        return paper
        
        
    def clean(self):
        cleaned_data = super(PaperForm, self).clean()   

        instance = super(PaperForm, self).save(commit=False)
        conference = instance.conference

        if conference.are_submissions_over:
            raise forms.ValidationError('The Submissions are over for now...')
            

        return cleaned_data
        
