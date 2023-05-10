from django import forms
from .models import Review, ReviewImage

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


class ReviewImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='리뷰 이미지 업로드',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'multiple': True,
            },
        ),
        required = False,
    )
    class Meta:
        model = ReviewImage
        fields = ('image',)