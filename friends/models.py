from django.db import models

# Create your models here.
from users.models import CustomUser


class Friend(models.Model):
    creator = models.ForeignKey(CustomUser, related_name="creator", on_delete=models.CASCADE)
    follower = models.ForeignKey(CustomUser, related_name="follower", on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return 'creator: '+ str(self.creator.username) + ' | ' + 'follower: ' + str(self.follower.username) + ' | ' + str(self.confirmed)
