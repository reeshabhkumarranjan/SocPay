from django.urls import path, include

from . import views

app_name = 'private_message'
urlpatterns = [
    path('friends_message/', views.friends_message, name='friends_message'), # sare grps display hote hai, leave, add, pending.
    path('chat/', views.chat, name='chat'),
]