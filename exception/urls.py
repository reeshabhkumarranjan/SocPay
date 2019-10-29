from django.urls import path
from . import views

app_name = 'exception'
urlpatterns = [
    path('error/', views.exception, name='exception')
]