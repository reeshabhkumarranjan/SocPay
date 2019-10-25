import datetime

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


class Transaction(models.Model):
    transaction_user_1 = models.ForeignKey(CustomUser, related_name='sender', on_delete=models.CASCADE, default=None)
    transaction_user_2 = models.ForeignKey(CustomUser, related_name='receiver', on_delete=models.CASCADE, default=None)
    transaction_amount = models.IntegerField(default=0)
    transaction_date = models.DateField(auto_now_add=True)
    transaction_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return 'U1: ' + str(self.transaction_user_1) + ' | ' + 'U2: ' + str(
            self.transaction_user_2) + ' | ' + 'Amount: ' + str(self.transaction_amount) + ' | ' + 'date: ' + str(
            self.transaction_date)
