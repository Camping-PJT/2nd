from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import os
from django.conf import settings


class User(AbstractUser):
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

    OWNER = '사장님'
    CUSTOMER = '고객님'
    USER_TYPE_CHOICES = [
        (OWNER, '사장님'),
        (CUSTOMER, '고객님'),
    ]
    
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    
    
    def profile_image_path(instance, filename):
        return f'profile/{instance.username}/{filename}'
    
    
    image = ProcessedImageField(upload_to=profile_image_path, blank=True, null=True)
    region = models.CharField(max_length=10, choices=REGION_CHOICES, default='서울')
    is_owner = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='고객님')
    address = models.CharField(max_length=200)


    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(User, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_user = User.objects.get(id=self.id)
            if self.image != old_user.image:
                if old_user.image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_user.image.path))
        super(User, self).save(*args, **kwargs)    
