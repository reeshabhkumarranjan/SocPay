from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('&<username>/friends/', views.Friendship.as_view(), name='friends'),
    path('&<username>/add/', views.add_friend, name='add_friend'),
    path('&<username>/cancel_request/', views.cancel, name='cancel_request'),
    path('&<username>/decline/', views.decline, name='decline'),
    path('&<username>/accept/', views.accept, name='accept'),
    path('&<username>/remove/', views.remove_friend, name='remove_friend'),
]
