from django.urls import path, include

from . import views

app_name = 'wallet'
urlpatterns = [
    path('wallet_home', views.wallet_home, name='wallet_home'),
    # path('transfer_money', views.transfer_money, name='transfer_money'),
    path('transfer', views.transfer, name='transfer'),
    path('make_changes', views.make_changes, name='make_changes'),
    path('transactions_to_be_accepted', views.transactions_to_be_accepted, name='transactions_to_be_accepted'),
    path('transactions_completed', views.transactions_completed, name='transactions_completed'),
    path('transactions_pending', views.transactions_pending, name='transactions_pending'),
    path('add_money', views.add_money, name='add_money'),
    # path('group', views.group, name='group'),
    path('add_money_work', views.add_money_work, name='add_money_work'),
    path('add_money_after_otp', views.add_money_after_otp, name='add_money_after_otp'),
    path('transaction_accept', views.transaction_accept, name='transaction_accept'),
    path('transaction_decline', views.transaction_decline, name='transaction_decline'),
    path('faltu', views.faltu, name='faltu'),
]