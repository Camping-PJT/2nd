from django import forms
from .models import Review
from ckeditor.widgets import CKEditorWidget

class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        label = False,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'리뷰제목',
                'class': 'form-box',
            }
        )
    )

    # content = forms.CharField(
    #     label = '리뷰 내용',
    #     widget = CKEditorWidget())

    
    class Meta:
        model = Review
        fields = ('title', 'content', )