from django import forms
from confucius.models import Paper, Conference, Domain


class PaperForm(forms.ModelForm):
    domains = forms.ModelMultipleChoiceField(Domain.objects.all(), required=True)

    class Meta:
        model = Paper
        exclude = ('submitter', 'conference', 'submission_date', 'last_update_date')

    def __init__(self, *args, **kwargs):
        pk_conference = kwargs.pop('pk_conference')
        super(PaperForm, self).__init__(*args, **kwargs)
        # Building domains, from an existing paper and a conference's id
        self.fields["domains"].queryset = Conference.objects.get(pk=pk_conference).domains
        paper = kwargs.pop('instance', None)
        if paper is not None:
            self.fields["domains"].initial = paper.domains.all()

    def save(self, **kwargs):
        paper = super(PaperForm, self).save(commit=False)

        # Update only one time these fields (during the creation)
        if paper.pk is None:
            paper.submitter = kwargs.pop('user')
            paper.conference = Conference.objects.get(pk=kwargs.pop('pk_conference'))
            paper.save()  # In order to get a primary key, for m2m relations (domains)

        paper.domains = self.cleaned_data['domains']
        paper.save()

        return paper
