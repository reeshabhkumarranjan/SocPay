from django.forms import ModelForm
from .models import Transaction


class transaction_form(ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_user_2', 'transaction_amount']

# class add_money_form(ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ['transaction_user_2', 'transaction_amount']
