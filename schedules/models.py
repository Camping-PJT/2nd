from django.db import models
from posts.models import Post
from django.conf import settings


class Schedule(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='schedules')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title
