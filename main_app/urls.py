from django.urls import path

from . import views

app_name = 'main_app'
urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),
    path('register_form', views.register_form, name='register_form'),
    path('login_form', views.login_form, name='login_form'),
]