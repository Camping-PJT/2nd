from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'name', 'email', 'image', 'is_owner', 'region',)
    
    REGION_CHOICES = [
        ('서울', '서울'), ('인천', '인천'), ('부산', '부산'), ('울산', '울산'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('세종', '세종'), ('제주도', '제주도'), ('경기도', '경기도'), ('강원도', '강원도'), ('충청북도', '충청북도'), ('충청남도', '충청남도'), ('전라북도', '전라북도'), ('전라남도', '전라남도'), ('경상북도', '경상북도'),('경상남도', '경상남도'),
    ]
    
    USER_TYPE_CHOICES = [
        ('사장님', '사장님'), ('고객', '고객'),
    ]
     
    username = forms.CharField(label='ID', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='비밀번호', label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='비밀번호 확인', label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    name = forms.CharField(label='이름', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='이메일', label_suffix='', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    region = forms.ChoiceField(label='선호지역', label_suffix='', choices=REGION_CHOICES, widget=forms.Select(
        attrs={'class': 'form-select'}))
    image = ProcessedImageField(
        spec_id='profile_image_thumbnail',
        processors=[ResizeToFill(70, 70)],
        format='JPEG',
        options={'quality': 200},
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        label='프로필 이미지',
        label_suffix='',
    )
    is_owner = forms.ChoiceField(label='사장님 여부', label_suffix='', choices=USER_TYPE_CHOICES, widget=forms.Select(
        attrs={'class': 'form-select'}))


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('image', 'email', 'is_owner', 'region',)
        
    REGION_CHOICES = [
        ('서울', '서울'), ('인천', '인천'), ('부산', '부산'), ('울산', '울산'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('세종', '세종'), ('제주도', '제주도'), ('경기도', '경기도'), ('강원도', '강원도'), ('충청북도', '충청북도'), ('충청남도', '충청남도'), ('전라북도', '전라북도'), ('전라남도', '전라남도'), ('경상북도', '경상북도'),('경상남도', '경상남도'),
    ]
    
    USER_TYPE_CHOICES = [
        ('사장님', '사장님'), ('고객', '고객'),
    ]
    
    email = forms.EmailField(label='이메일', label_suffix='', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    region = forms.ChoiceField(label='선호지역', label_suffix='', choices=REGION_CHOICES, widget=forms.Select(
        attrs={'class': 'form-select'}))
    image = ProcessedImageField(
        spec_id='profile_image_thumbnail',
        processors=[ResizeToFill(70, 70)],
        format='JPEG',
        options={'quality': 200},
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        label='프로필 이미지',
        label_suffix='',
    )
    is_owner = forms.ChoiceField(label='사장님 여부', label_suffix='', choices=USER_TYPE_CHOICES, widget=forms.Select(
        attrs={'class': 'form-select'}))
    address = forms.CharField(label='주소', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
 

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2',)
      
    old_password = forms.CharField(label='기존 비밀번호', label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='새 비밀번호', label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='새 비밀번호 확인', label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))