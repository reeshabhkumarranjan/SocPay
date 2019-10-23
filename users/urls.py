from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('friends/', views.Friendship.as_view(), name='friends'),
    path('add/', views.add_friend, name='add_friend'),
    path('cancel_request/', views.cancel, name='cancel_request'),
    path('decline/', views.decline, name='decline'),
    path('accept/', views.accept, name='accept'),
    path('remove/', views.remove_friend, name='remove_friend'),
]
