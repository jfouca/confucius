from django import forms
from confucius.models import Domain, Paper


class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ('title', 'description', 'file', 'co_authors', 'language', 'domains')
        widgets = {
            'domains': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(PaperForm, self).__init__(*args, **kwargs)

        self.fields['domains'].queryset = Domain.objects.filter(conferences__pk=self.instance.conference_id)
