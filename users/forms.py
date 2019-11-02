# users/forms.py
# from datetime import datetime, timedelta
import datetime

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import DateInput

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'username', 'email', 'date_of_birth')
        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'textfield'}),
            'username' : forms.TextInput(attrs={'class' : 'textfield'}),
            'email' : forms.EmailInput(attrs={'class' : 'textfield'}),
            'date_of_birth' : DateInput(attrs={'type':'date'})
        }
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        # print(date_of_birth, type(date_of_birth))
        # date_of_birth_python = datetime.date(date_of_birth)
        # print(date_of_birth + datetime.timedelta(days=4745))
        # print(datetime.datetime.now().date())
        if date_of_birth + datetime.timedelta(days=4745) > datetime.datetime.now().date():
            raise forms.ValidationError("You must be atleast 13 years old to join SocPay!")
        return date_of_birth
        # date_of_birth = forms.DateField(label="date_of_birth")
        #
        # def clean_date_of_birth(self):
        #     dob = self.fields['date_of_birth']
        #     print(dob)
        #     return dob

    def clean_email(self):
        email = self.cleaned_data['email']
        obj = CustomUser.objects.filter(email=email)
        if len(obj) > 0:
            raise forms.ValidationError("A user with this email already exists.")
        return email


class CustomUserChangeForm(UserChangeForm):
    captcha = CaptchaField()
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)
