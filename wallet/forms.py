from django.forms import ModelForm

from wallet.models import Transaction


class transaction_form(ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_user_2', 'transaction_amount']
