# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(default=datetime.now)
    website = models.URLField(default='')
    user_balance = models.IntegerField(default=0)
    user_type = models.CharField(max_length=30, default='')
    user_no_of_transactions = models.IntegerField(default=0)
    user_no_of_transactions_allowed = models.IntegerField(default=15)
    user_transactions_list = models.CharField(max_length=100000, default='') # TODO remove this list and change to a separate table

    def __str__(self):
        return 'name: ' + str(self.username) + ' | ' + 'balance: ' + str(self.user_balance) + ' | '


class Friend(models.Model):
    creator = models.ForeignKey(CustomUser, related_name="creator", on_delete=models.CASCADE)
    follower = models.ForeignKey(CustomUser, related_name="follower", on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
