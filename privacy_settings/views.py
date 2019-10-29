from datetime import datetime, timedelta

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from main_app import utils
from users.models import CustomUser
from wallet.utils import execute_transaction


def user_settings(request):
    return render(request, "user_settings.html")

def change_user_type(request):
    user_type = int(request.POST.get("user_type", "null"))
    if user_type < request.user.user_type or user_type > 5:
        raise SuspiciousOperation
    charge = 0
    if user_type == 2:
        charge = 50
    elif user_type == 3:
        charge = 100
    elif user_type == 4:
        charge = 150
    elif user_type == 5:
        charge = 5000
    if charge > request.user.user_balance:
        return utils.raise_exception(request, "Insufficient balance.")
    superuser = CustomUser.objects.get(is_superuser=True)
    execute_transaction(request.user, superuser, charge)
    request.user.user_type = user_type
    request.user.expiration_date = datetime.now() + timedelta(days=(30 if user_type != 5 else 365))
    request.user.save()
    return HttpResponseRedirect(reverse('privacy_settings:settings'))

def change_timeline_view_privacy(request):
    privacy_level = int(request.POST.get("timeline_privacy_level", "null"))
    request.user.timeline_view_level = privacy_level
    if privacy_level == 0:
        request.user.timeline_post_level = 0
    request.user.save()
    return HttpResponseRedirect(reverse('privacy_settings:settings'))

def change_timeline_post_privacy(request):
    privacy_level = int(request.POST.get("timeline_privacy_level", "null"))
    request.user.timeline_post_level = privacy_level
    request.user.save()
    return HttpResponseRedirect(reverse('privacy_settings:settings'))