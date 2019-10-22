from django.db import models
from users.models import CustomUser

# Create your models here.

class Post(models.Model):
    author_name = models.CharField(max_length=30)
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
    recipient_name = models.CharField(max_length=30)
    post_text = models.CharField(max_length=1000)
    # author_name = usermodel.BaseUser()
    # recipient_name = usermodel.BaseUser()
    # author_name_object = models.ForeignKey(CustomUser, related_name="author", on_delete=models.CASCADE)
    # recipient__name_object = models.ForeignKey(CustomUser, related_name="author", on_delete=models.CASCADE)

