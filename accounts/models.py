from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import os
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    REGION_CHOICES = [
        ('서울', '서울'), ('인천', '인천'), ('부산', '부산'), ('울산', '울산'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('세종', '세종'), ('제주도', '제주도'), ('경기도', '경기도'), ('강원도', '강원도'), ('충청북도', '충청북도'), ('충청남도', '충청남도'), ('전라북도', '전라북도'), ('전라남도', '전라남도'), ('경상북도', '경상북도'),('경상남도', '경상남도'),
    ]

    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    
    
    def profile_image_path(instance, filename):
        return f'profile/{instance.pk}/{filename}'
    
    
    image = ProcessedImageField(upload_to=profile_image_path, blank=True, null=True)
    region = models.CharField(max_length=10, choices=REGION_CHOICES, default='서울')
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