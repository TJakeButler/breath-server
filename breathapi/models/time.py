from django.db import models
from django.contrib.auth.models import User


class Time(models.Model):

    minutes = models.IntegerField()
    