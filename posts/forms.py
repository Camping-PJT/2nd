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
                'class': 'select--box',
                'style': 'width: 195px;'
            }
        )
    )
    title = forms.CharField(
        max_length=50, 
        label=False, 
        widget=forms.TextInput(
            attrs={
                'required': True,
                'placeholder': '캠핑장명(필수)',
                'class': 'form-box',
                'style': 'width: 400px; cursor:text;'
            }
        )
        
    )
    content = forms.CharField(
        label='내용(필수)',
        widget=forms.Textarea(
            attrs={
                'required': True,
                'placeholder': '캠핑장에 대한 자세한 내용을 입력해주세요.',
                'class': 'form-box',
                'style': 'width: 400px; cursor:text;'
            }
        )
    )

    # address = forms.CharField(
    #     max_length=200, 
    #     label='주소(필수)', 
    #     widget=forms.TextInput(
    #         attrs={
    #             'required': True, 
    #             'placeholder': '정확한 주소를 입력해주세요.', 
    #             'class': 'form-control',
    #             'style' : 'width: 600px;'
    #         }
    #     )
    # )
    category = forms.ChoiceField(
        choices=Post.CATEGORY_CHOICES, 
        label='카테고리(필수)', 
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'select--box',
                'style': 'width: 195px;'
            }
        )
    )
    # city = forms.ChoiceField(
    #     choices=Post.CITY_CHOICES, 
    #     label='지역(필수)', 
    #     widget=forms.Select(
    #         attrs={
    #             'required': True,
    #             'class': 'form-select',
    #             'style' : 'width: 600px;'
    #         }
    #     )
    # )
    phone = forms.CharField(
        max_length=14, 
        required = False,
        label='전화번호(필수)', 
        widget=forms.TextInput(
            attrs={
                'placeholder': '전화번호(필수) ex) 010-1234-5678',
                'class': 'form-box',
                'style': 'width: 400px; cursor:text;'
                
            }
        )
    )             
    open_hour = forms.TimeField(
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'class': 'form-box',
                'style': 'width: 195px; cursor:text;',
                'placeholder': '입실 시간 ex) 15:00',
            }
        ),
        input_formats=['%H:%M']
    )
    close_hour = forms.TimeField(
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'class': 'form-box',
                'style': 'width: 195px; cursor:text;',
                'placeholder': '퇴실 시간 ex) 11:00', 
            }
        ), 
        input_formats=['%H:%M']
    )

    extra_address = forms.CharField(
    max_length=100, 
    label=False,
    required=False,
    widget=forms.TextInput(
        attrs={
            'placeholder': '상세주소',
            'class': 'form-box',
            'style': 'width: 400px; cursor:text; margin-top:5px;'
            }
        )
    )


    class Meta:
        model = Post
        fields = ('category', 'nature', 'title', 'content', 'phone',  'open_hour', 'close_hour', 'tags', 'extra_address')
        widgets = {
            'tags': TagWidget(attrs={
                'class': 'form-box', 
                'style' : 'width: 400px;',
                'placeholder': "태그는 콤마(,)로 구분해주세요.",
                }),
        }
        labels = {
        'tags': '#해시태그(필수):',
        }
        help_texts = {
            'tags': '',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Retrieve the instance being edited
        instance = kwargs.get('instance')
        
        # Set the initial value for the address field
        if instance and instance.address:
            self.initial['address'] = instance.address


class FacilityForm(forms.ModelForm):
    FACILITY_CHOICES = Facility.FACILITY_CHOICES
    
    facilities = forms.MultipleChoiceField(
        label='편의시설',
        required=False,
        choices=FACILITY_CHOICES, 
        widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, post=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if post is not None:
            facility_values = post.facility_set.values_list('facility', flat=True)
            self.initial['facilities'] = list(facility_values)


    class Meta:
        model = Facility
        fields = ('facilities',)

class DeleteFacilityForm(forms.Form):
    delete_facilities = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='삭제할 편의시설 선택'
    )

    def __init__(self, post, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete_facilities'].choices = [
            (facility.pk, str(facility)) for facility in Facility.objects.filter(post=post)
        ]

    def clean_delete_facilities(self):
        delete_f_ids = self.cleaned_data.get('delete_facilities', [])
        return delete_f_ids



class CustomClearableFileInput(ClearableFileInput):
    template_name = 'posts/custom_clearable_file_input.html'

class PostImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='관련 이미지(필수)',
        widget=CustomClearableFileInput(
            attrs={
                'multiple': True, 
                'class': 'form-box', 
                'style': 'width: 400px;',
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