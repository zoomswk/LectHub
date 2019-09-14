from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=50, default="Untitled")
    author = models.CharField(max_length=50, default="Anonymous")
    video_url = models.CharField(max_length=100)
    rev_id = models.CharField(max_length=30)
    subtitle_url = models.CharField(max_length=100)
    def __str__(self):
        return str(self.title)
    objects = models.Manager()