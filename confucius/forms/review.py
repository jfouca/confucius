from django import forms
from confucius.models import Review


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ('title', 'detailed_commentary', 'commentary_for_president', 'overall_evaluation', 'reviewer_confidence',)
        
