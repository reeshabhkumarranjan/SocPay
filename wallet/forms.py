from django.forms import ModelForm

from friends.models import Friend
from wallet.models import Transaction


class transaction_form(ModelForm):
    def __init__(self, current_user, *args, **kwargs):
        super(transaction_form, self).__init__(*args, **kwargs)
        self.fields['transaction_user_2'].queryset = Friend.objects.filter(creator=current_user, confirmed=True) | Friend.objects.filter(follower=current_user, confirmed=True)

    class Meta:
        model = Transaction
        fields = ['transaction_user_2', 'transaction_amount']
