from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('username', 'name', 'phonenumber', 'email', 'region',
                  'address', 'image',)
        
    SEOUL = '서울'
    INCHEON = '인천'
    BUSAN = '부산'
    ULSAN = '울산'
    DAEGU = '대구'
    GWANGJU = '광주'
    DAEJEON = '대전'
    SEJONG = '세종'
    JEJU = '제주도'
    GYEONGGI = '경기도'
    GANGWON = '강원도'
    CHUNGBUK = '충청북도'
    CHUNGNAM = '충청남도'
    JEONBUK = '전라북도'
    JEONNAM = '전라남도'
    GYEONGBUK = '경상북도'
    GYEONGNAM = '경상남도'    
    REGION_CHOICES = [
        (SEOUL, '서울'), (INCHEON, '인천'), (BUSAN, '부산'), (ULSAN, '울산'), (DAEGU, '대구'), (GWANGJU, '광주'), (DAEJEON, '대전'), (SEJONG, '세종'), (JEJU, '제주도'), (GYEONGGI, '경기도'), (GANGWON, '강원도'), (CHUNGBUK, '충청북도'), (CHUNGNAM, '충청남도'), (JEONBUK, '전라북도'), (JEONNAM, '전라남도'), (GYEONGBUK, '경상북도'),(GYEONGNAM, '경상남도'),
    ]    

    username = forms.CharField(label='ID', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='비밀번호', label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='비밀번호 확인', label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    name = forms.CharField(label='이름', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    phonenumber = forms.CharField(label='전화번호', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='이메일', label_suffix='', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    region = forms.ChoiceField(label='사는 지역(시/도)', label_suffix='', choices=REGION_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control'}))

    address = forms.CharField(label='자세한 주소', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
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


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('phonenumber', 'email', 'region', 'address', 'image',)
        
    SEOUL = '서울'
    INCHEON = '인천'
    BUSAN = '부산'
    ULSAN = '울산'
    DAEGU = '대구'
    GWANGJU = '광주'
    DAEJEON = '대전'
    SEJONG = '세종'
    JEJU = '제주도'
    GYEONGGI = '경기도'
    GANGWON = '강원도'
    CHUNGBUK = '충청북도'
    CHUNGNAM = '충청남도'
    JEONBUK = '전라북도'
    JEONNAM = '전라남도'
    GYEONGBUK = '경상북도'
    GYEONGNAM = '경상남도'    
    REGION_CHOICES = [
        (SEOUL, '서울'), (INCHEON, '인천'), (BUSAN, '부산'), (ULSAN, '울산'), (DAEGU, '대구'), (GWANGJU, '광주'), (DAEJEON, '대전'), (SEJONG, '세종'), (JEJU, '제주도'), (GYEONGGI, '경기도'), (GANGWON, '강원도'), (CHUNGBUK, '충청북도'), (CHUNGNAM, '충청남도'), (JEONBUK, '전라북도'), (JEONNAM, '전라남도'), (GYEONGBUK, '경상북도'),(GYEONGNAM, '경상남도'),
    ]    

    phonenumber = forms.CharField(label='전화번호', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='이메일', label_suffix='', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    region = forms.ChoiceField(label='사는 지역(시/도)', label_suffix='', choices=REGION_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control'}))
    address = forms.CharField(label='자세한 주소', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    image = ProcessedImageField(
        spec_id='profile_image_thumbnail',
        processors=[ResizeToFill(70, 70)],
        format='JPEG',
        options={'quality': 90},
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        label='프로필 이미지',
        label_suffix='',
    )


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