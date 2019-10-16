# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import DateInput

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'username', 'email', 'date_of_birth')
        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'textfield'}),
            'username' : forms.TextInput(attrs={'class' : 'textfield'}),
            'email' : forms.EmailInput(attrs={'class' : 'textfield'}),
            'date_of_birth' : DateInput(attrs={'type':'date'})
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)
