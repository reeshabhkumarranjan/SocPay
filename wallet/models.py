from django.db import models

# Create your models here.
from users.models import CustomUser


class Transaction(models.Model):
    transaction_user_1 = models.ForeignKey(CustomUser,related_name='sender', on_delete=models.CASCADE, default=None)
    transaction_user_2 = models.ForeignKey(CustomUser,related_name='receiver', on_delete=models.CASCADE, default=None)
    transaction_amount = models.IntegerField(default=0);
    transaction_date = models.DateField(auto_now_add=True)
    transaction_time = models.TimeField(auto_now_add=True)
    transaction_accepted = models.BooleanField(default=False)

    def __str__(self):
        return 'U1: '+str(self.transaction_user_1) + ' | '+'U2: '+str(self.transaction_user_2)+' | '+'Amount: '+str(self.transaction_amount)+' | '+'date: '+str(self.transaction_date) + ' | ' + 'accepted: ' + str(self.transaction_accepted)
