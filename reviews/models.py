from django.db import models
from posts.models import Post
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone
from datetime import timedelta,datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = RichTextUploadingField(blank=True,null=True)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    emote_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='emote_reviews', through='Emote')

    def rate_to_star(self):
        return '★' * self.rating
    
    def rate_to_empty_star(self):
        return '☆' * (5 - self.rating)

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.strftime('%Y-%m-%d')
    
    def save(self, *args, **kwargs):
        self.post.rating = (self.post.rating*self.post.reviews.count() + self.rating) / (self.post.reviews.count() + 1)
        self.post.save()
        super(Review, self).save(*args, **kwargs)


class Emote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=10)