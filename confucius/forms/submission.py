from django import forms
from confucius.models import Paper, Domain, User


class PaperForm(forms.ModelForm):
    domains = forms.ModelMultipleChoiceField(Domain.objects.all(), required=True)
    submitter = forms.ModelMultipleChoiceField(User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Paper
        exclude = ('conference', 'submission_date', 'last_update_date')

    def __init__(self, *args, **kwargs):
        super(PaperForm, self).__init__(*args, **kwargs)
        # Building domains, from an existing paper and a conference's id
        self.fields["domains"].queryset = self.initial['conference'].domains

        if self.instance.pk is not None:
            self.fields["domains"].initial = self.instance.domains.all()
