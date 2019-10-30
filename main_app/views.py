import pyotp as pyotp
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime

from main_app import utils
from main_app.models import Post
from users.models import CustomUser
# from wallet.forms import transaction_form
from django.core.mail import send_mail


def register(request):
    """This just displays the register page."""
    return render(request, 'signup.html')


def login(request):
    """This just displays the register page."""
    if request.user.is_authenticated():
        return redirect('friends:timeline')
    return render(request, 'registration/login.html')


def index(request):
    return render(request, 'index.html')

# wallet

# def transfer_money(request):
#     # all_users = CustomUser.objects.all()
#     # context = {'all_users' : all_users}
#     return render(request, 'transfer_money.html', context=context)

# def group(request):
#     base_html = 'base.html'
#     if request.user.is_authenticated:
#         base_html = 'base_logged_in.html'
#     context = {'base_html': base_html, 'group_name': 'Sample Group', 'is_admin': False}
#
#     return render(request, 'group.html', context=context)
