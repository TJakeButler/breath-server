from django.db import models
from django.contrib.auth.models import User


class Journal(models.Model):

    entry = models.CharField(max_length=500)