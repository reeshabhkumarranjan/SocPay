from django.urls import path, include
from . import views

app_name = 'privacy_settings'
urlpatterns = [
    path('settings/', views.user_settings, name='settings'),
    path('upgrade/', views.change_user_type, name='upgrade'),
    path('update_timeline_view/', views.change_timeline_view_privacy, name='update_timeline_view'),
    path('update_timeline_post/', views.change_timeline_post_privacy, name='update_timeline_post'),
]