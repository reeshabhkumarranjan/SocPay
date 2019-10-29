# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils.timezone import now


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(default=datetime.now)
    website = models.URLField(default='')
    user_balance = models.IntegerField(default=40)
    user_type = models.IntegerField(default=1)
    user_no_of_transactions = models.IntegerField(default=0)
    user_no_of_transactions_allowed = models.IntegerField(default=15)
    user_transactions_list = models.CharField(max_length=100000, default='') # TODO remove this list and change to a separate table
    expiration_date = models.DateTimeField(auto_now_add=True)
    timeline_view_level = models.IntegerField(default=0)
    timeline_post_level = models.IntegerField(default=0)

    def __str__(self):
        return 'name: ' + str(self.username) + ' | ' + 'balance: ' + str(self.user_balance) + ' | '


