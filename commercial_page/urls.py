from django.urls import path, include

from . import views

app_name = 'commercial_page'
urlpatterns = [
    path('page_list/', views.page_list, name='page_list'), # for page admins
    path('page_timeline/<int:page_id>', views.page_timeline, name='page_timeline'),
    path('add_post/', views.add_post, name='add_post'),
    path('page_list_global/', views.page_list_global, name='page_list_global'),
    path('add_page/', views.add_page, name='add_page'),
    path('add_page_form/', views.add_page_form, name='add_page_form'),
]
