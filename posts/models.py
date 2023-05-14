from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from django.core.validators import RegexValidator
from django.conf import settings
import os
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, MaxValueValidator


class Post(models.Model):
    WILD = '오지, 노지'
    PAID = '유료'
    GLAMPING = '글램핑, 카라반'
    CATEGORY_CHOICES = [(WILD, '오지, 노지'), (PAID, '유료'), (GLAMPING, '글램핑, 카라반')]
    VALLEY = '계곡'
    SEA = '바다'
    MOUNTAIN = '산'
    RIVERSIDE = '강변'
    LAKE = '호수'
    NATURE_CHOICES = [(VALLEY, '계곡'), (SEA, '바다'), (MOUNTAIN, '산'), (RIVERSIDE, '강변'), (LAKE, '호수')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    visit_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='visit_posts')
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    city = models.CharField(max_length=10)
    nature = models.CharField(max_length=10, choices=NATURE_CHOICES)
    address = models.CharField(max_length=200)
    extra_address = models.CharField(max_length=200)
    phoneNumberRegex = RegexValidator(regex=r'^0[1-9]\d{0,2}-\d{3,4}-\d{4}$')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=14)
    open_hour = models.TimeField()
    close_hour = models.TimeField()
    tags = TaggableManager()
    rating = models.DecimalField(default=0, max_digits=5, decimal_places=1)
    priorities = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='priorities')

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kargs):
        images = self.postimage_set.all()
        for image in images:
            image.delete()
        super(Post, self).delete(*args, **kargs)


class Facility(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    WIFI =  '와이파이'
    STORE = '매점'
    SHOWER = '샤워시설'
    ELECTRO =  '전기'
    WARM = '온수제공'
    LEND = '대여'
    WOOD = '장작'
    SINK = '개수대'
    TOILET = '화장실'
    FACILITY_CHOICES = [(WIFI, '와이파이'), (STORE, '매점'), (SHOWER, '샤워시설'), (ELECTRO, '전기'), (WARM, '온수제공'), (LEND, '대여'), (WOOD, '장작'), (SINK, '개수대'), (TOILET, '화장실')]
    facility = models.CharField(max_length=10, choices=FACILITY_CHOICES)
    def __str__(self):
        return self.get_facility_display()

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def post_image_path(instance, filename):
        return f'post/{instance.post.pk}/{filename}'
    image = ProcessedImageField(
        upload_to=post_image_path,
        blank=True, 
        null=True)
    
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(PostImage, self).delete(*args, **kargs)


class Priority(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        ordering = ['priority']