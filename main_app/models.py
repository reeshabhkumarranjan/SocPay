from django.contrib.auth.models import AbstractUser
from django.db import models
from users import models as usermodel

# Create your models here.

class Post(models.Model):
    author_name = usermodel.BaseUser()
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
    recipient_name = usermodel.BaseUser()
    post_text = models.CharField(max_length=1000)