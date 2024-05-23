from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    albums = models.IntegerField()
    tracks = models.IntegerField()
    self = models.CharField(max_length=100)