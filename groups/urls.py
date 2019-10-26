from django.urls import path, include

from . import views

app_name = 'groups'
urlpatterns = [
    path('group/', views.ShowGroups.as_view(), name='group'), # sare grps display hote hai, leave, add, pending.
    path('admin/', views.MyGroups.as_view(), name='group_admin'), # my owned group. btton of groups.
    path('view/', views.groupsView, name='group_view'), #
    path('add/', views.addgroup, name='add_group'), #
    path('join/', views.AddJoinRequest, name='join_group'), #
    path('cancel/', views.cancelJoinRequest, name='cancel_request'),
    path('remove/', views.removeFromGroup, name='remove'),
    path('accept/', views.acceptJoinRequest, name='accept'),
    path('decline/', views.rejectJoinRequest, name='decline'),
]
