from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        label = '리뷰 제목',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    content = forms.CharField(
        label = '리뷰 내용',
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
            }
        )
    )
    
    rating = forms.IntegerField(
        label = '평점',
        widget = forms.Select(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    class Meta:
        model = Review
        fields = ('title', 'content', 'rating', )