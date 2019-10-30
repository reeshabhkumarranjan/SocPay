from django.forms import ModelForm

from friends.models import Friend
from main_app.utils import get_friends
from wallet.models import Transaction


# class transaction_form(ModelForm):
#     def __init__(self, current_user, *args, **kwargs):
#         super(transaction_form, self).__init__(*args, **kwargs)
#         print(type(current_user))
#         print(current_user)
#         try:
#             friends = get_friends(current_user)
#             self.fields['transaction_user_2'].queryset = friends
#         except:
#             self.fields['transaction_user_2'].queryset =
#             return
#
#     class Meta:
#         model = Transaction
#         fields = ['transaction_user_2', 'transaction_amount']