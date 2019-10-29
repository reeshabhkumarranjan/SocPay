from django.urls import path, include
from . import views

app_name = 'privacy_settings'
urlpatterns = [
    path('settings/', views.user_settings, name='settings'),
    path('upgrade/', views.change_user_type, name='upgrade'),
]