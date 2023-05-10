from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        label = '리뷰 제목',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
            }
        ),
        required= True
    )
    
    
    rating = forms.ChoiceField(
        label = '평점',
        widget = forms.Select(
            attrs = {
                'class': 'form-control'
            }
        ),
        choices = ((1, 1), (1, 2), (3, 3), (4, 4), (5, 5)),
        required= True,
    )
    class Meta:
        model = Review
        fields = ('title', 'content', 'rating', )