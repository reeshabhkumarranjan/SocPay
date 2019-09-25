from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('index', views.index, name='index')
]