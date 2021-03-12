from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):

    name = models.CharField(max_length=255)
    inhale = models.IntegerField()
    exhale = models.IntegerField()
    hold = models.IntegerField()
    