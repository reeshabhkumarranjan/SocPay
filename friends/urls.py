from django.urls import path
from . import views

app_name = 'friends'
urlpatterns = [
    path('timeline', views.timeline, name='timeline'),
    path('friends', views.friends, name='friends'),
    path('add_post', views.add_post, name='add_post'),
    path('friend_timeline/<slug:friend_username>', views.friend_timeline, name='friend_timeline'),
    path('add_post_friend/<slug:friend_username>', views.add_post_friend, name='add_post_friend'),
]