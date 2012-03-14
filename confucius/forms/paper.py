from django import forms
from confucius.models import Domain, Language, Membership, Paper, Role


class PaperForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'description', 'file', 'co_authors', 'language', 'domains')
        model = Paper
        widgets = {
            'domains': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(PaperForm, self).__init__(*args, **kwargs)

        self.fields['domains'].help_text = ""
        self.fields['language'].queryset = Language.objects.all().order_by('name')
        self.fields['domains'].queryset = Domain.objects.filter(conferences__pk=self.instance.conference_id)

    def save(self, commit=True):
        paper = super(PaperForm, self).save(commit)

        membership, created = Membership.objects.get_or_create(user=paper.submitter, conference=paper.conference)
        membership.roles.add(Role.objects.get(code='S'))
        membership.set_last_accessed()

        return paper

    def clean(self):
        cleaned_data = super(PaperForm, self).clean()

        instance = self.instance
        conference = instance.conference

        if conference.are_submissions_over == True:
            raise forms.ValidationError('The Submissions are over for now.')

        if conference.are_submissions_notstarted == True:
            raise forms.ValidationError('The Submissions are not started.')

        return cleaned_data
