from django.urls import path, include

from . import views

app_name = 'commercial_page'
urlpatterns = [
    path('page_list/', views.page_list, name='page_list'),
    path('page_timeline/<int:page_id>', views.page_timeline, name='page_timeline'),
    path('add_post/', views.add_post, name='add_post')
]
