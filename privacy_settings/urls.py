from django.urls import path, include
from . import views

app_name = 'privacy_settings'
urlpatterns = [
    path('settings/', views.user_settings, name='settings'),
    path('upgrade/', views.change_user_type, name='upgrade'),
    path('update_timeline_view/', views.change_timeline_view_privacy, name='update_timeline_view'),
    path('update_timeline_post/', views.change_timeline_post_privacy, name='update_timeline_post'),
    path('group_settings/<int:group_id>', views.group_settings, name='group_settings'),
    path('update_group_details', views.update_group_details, name='update_group_details'),
    path('update_member_deletion_access/', views.update_member_deletion_access, name='update_member_deletion_access'),
]