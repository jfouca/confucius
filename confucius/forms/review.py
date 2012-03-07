from django import forms
from confucius.models import Review


class ProblemForm(forms.Form):
    problem = forms.CharField(label=u'Problem', help_text=u'Please indicate in a concise way the exact problem with the paper.',
            min_length=12, widget=forms.Textarea(attrs={'class': 'input-xlarge'}))


class ReviewForm(forms.ModelForm):
    confidence_choice = (('1', 'Null'), ('2', 'Low'), ('3', 'Medium'), ('4', 'High'), ('5', 'Expert'))
    reviewer_confidence = forms.TypedChoiceField(coerce=int, choices=confidence_choice, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ( 'detailed_commentary', 'commentary_for_president', )

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        review = kwargs.pop('instance', None)
        if review is not None:
            self.fields["reviewer_confidence"].initial = review.reviewer_confidence
        else:
            self.fields["reviewer_confidence"].initial = '0'

    def save(self, **kwargs):
        review = super(ReviewForm, self).save(commit=False)
        review.reviewer_confidence = self.cleaned_data['reviewer_confidence']
        evaluation = kwargs.pop('overall_evaluation', None)
        review.overall_evaluation = evaluation
        review.save()
        return review

    def clean(self):
        cleaned_data = super(ReviewForm, self).clean()

        instance = self.instance

        conference = instance.assignment.all()[0].conference

        if conference.are_reviews_over == True:
            raise forms.ValidationError('The Reviews are over for now.')
            
        if conference.are_reviews_notstarted == True:
            raise forms.ValidationError('The Reviews are not started.')

        return cleaned_data
