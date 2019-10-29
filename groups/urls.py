from django.urls import path, include

from . import views

app_name = 'groups'
urlpatterns = [
    path('group/', views.show_groups, name='group'), # sare grps display hote hai, leave, add, pending.
    path('admin/', views.showMyGroups, name='group_admin'), # my owned group. btton of groups.
    path('view/<int:group_id>', views.groupsView, name='group_view'), #
    path('add/', views.addgroup, name='add_group'), #
    path('join/', views.AddJoinRequest, name='join_group'), #
    path('cancel/', views.cancelJoinRequest, name='cancel_request'),
    path('remove/', views.removeFromGroup, name='remove'),
    path('accept/', views.acceptJoinRequest, name='accept'),
    path('decline/', views.rejectJoinRequest, name='decline'),
    path('add_group_post/', views.add_group_post, name='add_group_post'),
    path('remove_other/', views.remove_other_from_group, name='remove_other'),
    path('after_otp/', views.after_otp, name="after_otp"),
    # path('update_member_deletion_access/')
]
