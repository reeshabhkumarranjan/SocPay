from django.urls import path, include

from . import views

app_name = 'private_message'
urlpatterns = [
    path('friends_message/', views.friends_message, name='friends_message'), # sare grps display hote hai, leave, add, pending.
    path('chat/', views.chat, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
    path('friends_message_username/<slug:friend_username>', views.friends_message_username, name='friends_message_username'),
]