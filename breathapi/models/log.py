from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    journal = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    time = models.ForeignKey("Time", on_delete=models.CASCADE)