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
    expiration_date = models.DateTimeField(auto_now_add=True)
    timeline_view_level = models.IntegerField(default=0)
    timeline_post_level = models.IntegerField(default=0)
    user_last_transaction_for_begin = models.CharField(max_length=1000,
                                                       default=datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
    user_last_transaction_for_otp = models.CharField(max_length=1000,
                                                     default=datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
    verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)


