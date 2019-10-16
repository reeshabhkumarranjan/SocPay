from django.db import models

# Create your models here.

class Post(models.Model):
    # author_name = usermodel.BaseUser()
    author_name = models.CharField(max_length=30)
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
    # recipient_name = usermodel.BaseUser()
    recipient_name = models.CharField(max_length=30)
    post_text = models.CharField(max_length=1000)