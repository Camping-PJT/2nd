from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill
from django import forms
from django.forms.widgets import ClearableFileInput



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'last_name', 'email', 'image', 'is_owner', 'region',)
    
    REGION_CHOICES = [
        ('서울', '서울'), ('인천', '인천'), ('부산', '부산'), ('울산', '울산'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('세종', '세종'), ('제주도', '제주도'), ('경기도', '경기도'), ('강원도', '강원도'), ('충청북도', '충청북도'), ('충청남도', '충청남도'), ('전라북도', '전라북도'), ('전라남도', '전라남도'), ('경상북도', '경상북도'),('경상남도', '경상남도'),
    ]
    
    USER_TYPE_CHOICES = [
        ('사장님', '사장님'), ('고객님', '고객님'),
    ]
    username = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-box','placeholder' : '아이디','style' : 'width:400px;'}))
    password1 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-box','placeholder' : '비밀번호','style' : 'width:400px;'}))
    password2 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-box','placeholder' : '비밀번호 확인','style' : 'width:400px;'}))
    last_name = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-box','placeholder' : '이름','style' : 'width:400px;'}))
    email = forms.EmailField(label=False, label_suffix='', widget=forms.EmailInput(
        attrs={'class': 'form-box','placeholder' : '이메일','style' : 'width:400px;'}))
    region = forms.ChoiceField(label='선호지역', label_suffix='', choices=REGION_CHOICES, widget=forms.Select(
        attrs={'class': 'select--box','style' : 'width:195px;'}))
    image = ProcessedImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-box','style' : 'width:400px;'}),
        label='프로필 이미지',
        label_suffix='',
        spec_id='image_size',
    )
    is_owner = forms.ChoiceField(label='유저 타입', label_suffix='', choices=USER_TYPE_CHOICES, widget=forms.Select(
        attrs={'class': 'select--box','style' : 'width:195px;'}))

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'posts/custom_clearable_file_input.html'

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('last_name', 'image', 'email', 'is_owner', 'region',)
    last_name = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-box','placeholder' : '이름','style' : 'width:400px;'}))
    
    REGION_CHOICES = [
        ('서울', '서울'), ('인천', '인천'), ('부산', '부산'), ('울산', '울산'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('세종', '세종'), ('제주도', '제주도'), ('경기도', '경기도'), ('강원도', '강원도'), ('충청북도', '충청북도'), ('충청남도', '충청남도'), ('전라북도', '전라북도'), ('전라남도', '전라남도'), ('경상북도', '경상북도'),('경상남도', '경상남도'),
    ]
    
    USER_TYPE_CHOICES = [
        ('사장님', '사장님'), ('고객님', '고객님'),
    ]
    
    email = forms.EmailField(label='이메일', label_suffix='', widget=forms.EmailInput(
        attrs={'class': 'form-box','placeholder' : '이메일','style' : 'width:400px;'}))
    region = forms.ChoiceField(label='선호지역', label_suffix='', choices=REGION_CHOICES, widget=forms.Select(
        attrs={'class': 'select--box','style' : 'width:195px;'}))
    image = ProcessedImageField(
        required=False,
        widget=CustomClearableFileInput(attrs={'class': 'form-box','style' : 'width:400px;'}),
        label='프로필 이미지',
        label_suffix='',
        spec_id='image_size',
    )

    is_owner = forms.ChoiceField(label='유저 타입', label_suffix='', choices=USER_TYPE_CHOICES, widget=forms.Select(
        attrs={'class': 'select--box','style' : 'width:195px;'}))
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
 

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2',)
    old_password = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-box','placeholder' : '기존 비밀번호','style' : 'width:400px;'}))
    new_password1 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-box','placeholder' : '새 비밀번호','style' : 'width:400px;'}))
    new_password2 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-box','placeholder' : '새 비밀번호 확인','style' : 'width:400px;'}))
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-box',
                'placeholder' : '아이디',
                'style' : 'width:400px;'
            }
        )
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-box',
                'placeholder' : '비밀번호',
                'style' : 'width:400px;'
            }
        )
    )
    

