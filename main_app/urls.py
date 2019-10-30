from django.urls import path

from . import views

app_name = 'main_app'
urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
]