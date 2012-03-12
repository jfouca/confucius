from django import forms
from confucius.models import Review


class ProblemForm(forms.Form):
    problem = forms.CharField(label=u'Enter your explanation', help_text=u'Please indicate in a concise way the exact problem with the paper or the assignment.',
            min_length=12, widget=forms.Textarea(attrs={'class': 'input-xlarge'}))


class ReviewForm(forms.ModelForm):
    confidence_choice = (('1', 'Null'), ('2', 'Low'), ('3', 'Medium'), ('4', 'High'), ('5', 'Expert'))
    reviewer_confidence = forms.TypedChoiceField(coerce=int, choices=confidence_choice, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ( 'detailed_commentary', 'commentary_for_president', )

    def __init__(self, *args, **kwargs):
        enable_reviewer_confidence = kwargs.pop('enable_reviewer_confidence', None)
        super(ReviewForm, self).__init__(*args, **kwargs)
        review = kwargs.pop('instance', None)
        
	self.fields["reviewer_confidence"].initial = '0'
        if review is not None:
            self.fields["reviewer_confidence"].initial = review.reviewer_confidence
            
	if not enable_reviewer_confidence:
	    del self.fields["reviewer_confidence"]


    def save(self, **kwargs):
        review = super(ReviewForm, self).save(commit=False)
        evaluation = kwargs.pop('overall_evaluation', None)
        enable_reviewer_confidence = kwargs.pop('enable_reviewer_confidence', None)
        review.overall_evaluation = evaluation
        
        if enable_reviewer_confidence:
	    review.reviewer_confidence = self.cleaned_data['reviewer_confidence']
        else:
	    review.reviewer_confidence = 0
        
        review.save()
        return review

    def clean(self):
        cleaned_data = super(ReviewForm, self).clean()

        instance = self.instance

        conference = instance.get_assignment().conference

        if conference.are_reviews_over == True:
            raise forms.ValidationError('The Reviews are over for now.')
            
        if conference.are_reviews_notstarted == True:
            raise forms.ValidationError('The Reviews are not started.')

        return cleaned_data
