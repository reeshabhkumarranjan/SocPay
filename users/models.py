# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(default=datetime.now)
    website = models.URLField(default='')


class Friend(models.Model):
    creator = models.ForeignKey(CustomUser, related_name="creator", on_delete=models.CASCADE)
    follower = models.ForeignKey(CustomUser, related_name="follower", on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)