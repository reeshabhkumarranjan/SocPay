from django.urls import path

from . import views

app_name = 'main_app'
urlpatterns = [
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('timeline', views.timeline, name='timeline'),
    path('friends', views.friends, name='friends'),
    path('add_post', views.add_post, name='add_post'),
    path('friend_timeline/<slug:friend_username>', views.friend_timeline, name='friend_timeline'),
    path('add_post_friend/<slug:friend_username>', views.add_post_friend, name='add_post_friend'),
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
    path('transaction_accept', views.transaction_accept, name='transaction_accept'),
    path('transaction_decline', views.transaction_decline, name='transaction_decline'),
]