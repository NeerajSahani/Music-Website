from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100, blank=True, null=True)
    image = models.FileField(upload_to='album', blank=True, null=True)
    genre = models.CharField(max_length=20, default='slow')
    released = models.DateField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music:AlbumView', kwargs={'pk': self.pk})


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=100)
    song_artist = models.CharField(max_length=100, blank=True, null=True)
    duration = models.DecimalField(max_digits=4, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    song = models.FileField(upload_to='song')
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.song_name

    def get_absolute_url(self):
        return reverse('music:AlbumView', kwargs={'pk': self.album.id})


class LikeSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
