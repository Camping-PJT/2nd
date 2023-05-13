from django import forms
from .models import Review
from ckeditor.widgets import CKEditorWidget

class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        label = '리뷰 제목',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    # content = forms.CharField(
    #     label = '리뷰 내용',
    #     widget = CKEditorWidget())

    
    class Meta:
        model = Review
        fields = ('title', 'content', )