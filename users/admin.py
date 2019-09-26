from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from users.forms import BaseUserCreationForm, BaseUserChangeForm
from users.models import BaseUser


class BaseUserAdmin(UserAdmin):
    add_form = BaseUserCreationForm
    form = BaseUserChangeForm
    model = BaseUser
    list_display = ['email', 'username']


admin.site.register(BaseUser, BaseUserAdmin)
