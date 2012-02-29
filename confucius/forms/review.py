from django import forms
from confucius.models import Review


class ReviewForm(forms.ModelForm):

    evaluation_choice = (('1', 'Strong reject'), ('2', 'Reject'), ('3', 'Weak reject'), ('4', 'Bordeline paper'), \
                            ('5', 'Weak accept'), ('6', 'Accept'), ('7', 'Strong accept'))
    overall_evaluation = forms.TypedChoiceField(coerce=int, choices=evaluation_choice, widget=forms.RadioSelect)
    confidence_choice = (('1', 'Null'), ('2', 'Low'), ('3', 'Medium'), ('4', 'High'), ('5', 'Expert'))
    reviewer_confidence = forms.TypedChoiceField(coerce=int, choices=confidence_choice, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ('title', 'detailed_commentary', 'commentary_for_president', )
        
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        review = kwargs.pop('instance', None)
        if review is not None:
            self.fields["overall_evaluation"].initial = review.overall_evaluation
            self.fields["reviewer_confidence"].initial = review.reviewer_confidence
        else:
            self.fields["overall_evaluation"].initial = '4'
            self.fields["reviewer_confidence"].initial = '3'
            
    
    def save(self, **kwargs):
        review = super(ReviewForm, self).save(commit=False)
        review.overall_evaluation = self.cleaned_data['overall_evaluation']
        review.reviewer_confidence = self.cleaned_data['reviewer_confidence']
        review.save()
        return review
        


