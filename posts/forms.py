from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Post, PostImage, Facility
from taggit.forms import TagField, TagWidget
from taggit.managers import TaggableManager
from django.conf import settings
import os

class PostForm(forms.ModelForm):
    nature = forms.ChoiceField(
        choices=Post.NATURE_CHOICES,
        label='환경(필수)',
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-select',
                'style': 'width: 600px;'
            }
        )
    )
    title = forms.CharField(
        max_length=50, 
        label='캠핑장명(필수)', 
        widget=forms.TextInput(
            attrs={
                'required': True,
                'placeholder': '캠핑장명을 입력해주세요.',
                'class': 'form-control',
                'style' : 'width: 600px;'
            }
        )
        
    )
    content = forms.CharField(
        label='내용(필수)',
        widget=forms.Textarea(
            attrs={
                'required': True,
                'placeholder': '기타 내용을 입력해주세요.',
                'class': 'form-control',
                'style': 'width: 600px;'
            }
        )
    )

    address = forms.CharField(
        max_length=200, 
        label='주소(필수)', 
        widget=forms.TextInput(
            attrs={
                'required': True, 
                'placeholder': '정확한 주소를 입력해주세요.', 
                'class': 'form-control',
                'style' : 'width: 600px;'
            }
        )
    )
    category = forms.ChoiceField(
        choices=Post.CATEGORY_CHOICES, 
        label='카테고리(필수)', 
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-select',
                'style' : 'width: 600px;'
            }
        )
    )
    city = forms.ChoiceField(
        choices=Post.CITY_CHOICES, 
        label='지역(필수)', 
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-select',
                'style' : 'width: 600px;'
            }
        )
    )
    phone = forms.CharField(
        max_length=14, 
        required = False,
        label='전화번호(필수)', 
        widget=forms.TextInput(
            attrs={
                'placeholder': '-을 포함해주세요.',
                'class': 'form-control',
                'style' : 'width: 600px;'
                
            }
        )
    )             
    open_hour = forms.TimeField(
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'class': 'form-control',
                'style' : 'width: 600px;'
                
            }
            ),
        input_formats=['%H:%M']
    )
    close_hour = forms.TimeField(
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'class': 'form-control',
                'style' : 'width: 600px;'
                
            }
        ), 
        input_formats=['%H:%M']
    )


    class Meta:
        model = Post
        fields = ('category', 'nature', 'city', 'title', 'content', 'address', 'phone',  'open_hour', 'close_hour', 'tags')
        widgets = {
            'tags': TagWidget(attrs={
                'class': 'form-control', 
                'style' : 'width: 600px;',
                'placeholder': "태그는 콤마(,)로 구분해주세요.",
                }),
        }
        labels = {
        'tags': '#해시태그(필수):',
        }
        help_texts = {
            'tags': '',
        }


class FacilityForm(forms.ModelForm):
    FACILITY_CHOICES = Facility.FACILITY_CHOICES
    facilities = forms.MultipleChoiceField(choices=FACILITY_CHOICES, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Facility
        fields = ('facilities',)



class CustomClearableFileInput(ClearableFileInput):
    template_name = 'posts/custom_clearable_file_input.html'

class PostImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='관련 이미지(필수)',
        widget=CustomClearableFileInput(
            attrs={
                'multiple': True, 
                'class': 'form-control', 
                'style': 'width: 600px;',
            }
        ),
    )

    class Meta:
        model = PostImage
        fields = ('image',)

class DeleteImageForm(forms.Form):
    delete_images = forms.MultipleChoiceField(
        label='삭제할 이미지 선택',
        required = False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )

    def __init__(self, post, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete_images'].choices = [
            (image.pk, image.image.name) for image in PostImage.objects.filter(post=post)
        ]

    def clean(self):
        cleaned_data = super().clean()
        delete_ids = cleaned_data.get('delete_images')
        if delete_ids:
            images = PostImage.objects.filter(pk__in=delete_ids)
            for image in images:
                os.remove(os.path.join(settings.MEDIA_ROOT, image.image.path))
            images.delete()