from django.urls import path

from . import views

app_name = 'main_app'
urlpatterns = [
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('timeline', views.timeline, name='timeline'),
    path('friends', views.friends, name='friends')
]