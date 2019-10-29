from django.forms import ModelForm

from friends.models import Friend
from main_app.utils import get_friends
from wallet.models import Transaction


class transaction_form(ModelForm):
    def __init__(self, current_user, *args, **kwargs):
        super(transaction_form, self).__init__(*args, **kwargs)
        friends = get_friends(current_user)
        # id_list = [friend.id for friend in friends]
        # friends = Friend.objects.filter(pk__in=id_list)
        self.fields['transaction_user_2'].queryset = friends
    class Meta:
        model = Transaction
        fields = ['transaction_user_2', 'transaction_amount']