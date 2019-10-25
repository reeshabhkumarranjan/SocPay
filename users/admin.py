# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Friend


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['first_name', 'email', 'username', 'date_of_birth', 'user_type', 'user_balance']
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('user_type', 'user_balance')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Friend)