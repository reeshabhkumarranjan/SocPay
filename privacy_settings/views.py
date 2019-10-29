from datetime import datetime, timedelta

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from groups.models import Groups
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
    request.user.user_balance -= charge
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

def group_settings(request, group_id):
    group = Groups.objects.get(id=group_id)
    context = {'group' : group}
    return render(request, 'group_settings.html', context=context)

def update_group_details(request):
    group_id = request.POST.get("group_id", "null")
    group = Groups.objects.get(id=group_id)
    group_name = request.POST.get("group_name", "null")
    group_description = request.POST.get("group_description", "null")
    group_fees = int(request.POST.get("group_fees", "null"))
    group.group_name = group_name
    group.description = group_description
    group.fees = group_fees
    group.save()
    return HttpResponseRedirect(reverse('privacy_settings:group_settings', kwargs={'group_id' : group_id}))

def update_member_deletion_access(request):
    group_id = request.POST.get("group_id", "null")
    group = Groups.objects.get(id = group_id)
    member_deletion_access = int(request.POST.get("member_deletion_access", "null"))
    group.member_deletion_access = member_deletion_access
    group.save()
    return HttpResponseRedirect(reverse('privacy_settings:group_settings', kwargs={'group_id': group_id}))

def update_post_view_access(request): # actually it restricts from showing the whole group
    group_id = request.POST.get("group_id", "null")
    group = Groups.objects.get(id = group_id)
    post_view_access = int(request.POST.get("post_view_access", "null"))
    group.post_view_access = post_view_access
    group.save()
    return HttpResponseRedirect(reverse('privacy_settings:group_settings', kwargs={'group_id': group_id}))
