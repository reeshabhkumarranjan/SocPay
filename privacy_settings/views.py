from datetime import datetime, timedelta

import django
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.core.mail import send_mail
from django.db import DatabaseError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from groups.models import Groups, Group_Members, isAdmin
from groups.views import group_exists
from main_app import utils
from users.models import CustomUser
from wallet.models import Transaction
from wallet.utils import execute_transaction, getOTP


def user_settings(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    return render(request, "user_settings.html")

def change_user_type(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    user_type = 0
    try:
        user_type = int(request.POST.get("user_type", "null"))
    except:
        raise PermissionDenied
    if user_type not in [1, 2, 3, 4, 5]:
        raise PermissionDenied
    if user_type < request.user.user_type or user_type > 5:
        raise PermissionDenied
    charge = 0
    allowed_number_of_transaction = 15
    if user_type == 2:
        charge = 50
        allowed_number_of_transaction = 30
    elif user_type == 3:
        charge = 100
        allowed_number_of_transaction = 30
    elif user_type == 4:
        charge = 150
        allowed_number_of_transaction = 30
    elif user_type == 5:
        charge = 5000
        allowed_number_of_transaction = 2147483646
    if charge > request.user.user_balance:
        return utils.raise_exception(request, "Insufficient balance.")
    if user_type == 5 and not request.user.verified:
        return utils.raise_exception(request, "You need to be verified to upgrade to a commercial user.")
    superuser = None
    try:
        superuser = CustomUser.objects.get(username="admin")
    except:
        raise DatabaseError
    # raise DatabaseError
    execute_transaction(request.user, superuser, charge)
    request.user.user_balance -= charge
    request.user.user_type = user_type
    request.user.expiration_date = datetime.now() + timedelta(days=(30 if user_type != 5 else 365))
    request.user.user_no_of_transactions_allowed = allowed_number_of_transaction
    request.user.save()
    return HttpResponseRedirect(reverse('privacy_settings:settings'))

def change_timeline_view_privacy(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    privacy_level = 0
    try:
        privacy_level = int(request.POST.get("timeline_privacy_level", "null"))
    except:
        raise PermissionDenied
    if privacy_level not in [0, 1]:
        raise PermissionDenied
    request.user.timeline_view_level = privacy_level
    if privacy_level == 0:
        request.user.timeline_post_level = 0
    request.user.save()
    return HttpResponseRedirect(reverse('privacy_settings:settings'))

def change_timeline_post_privacy(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    privacy_level = 0
    try:
        privacy_level = int(request.POST.get("timeline_privacy_level", "null"))
    except:
        raise PermissionDenied
    if privacy_level not in [0, 1]:
        raise PermissionDenied
    request.user.timeline_post_level = privacy_level
    request.user.save()
    return HttpResponseRedirect(reverse('privacy_settings:settings'))

def group_settings(request, group_id):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if not group_exists(group_id):
        raise PermissionDenied
    group = Groups.objects.get(id=group_id)
    if not isAdmin(request.user, group):
        raise PermissionDenied
    context = {'group' : group}
    return render(request, 'group_settings.html', context=context)

def update_group_details(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    group_id = request.POST.get("group_id", "null")
    if not group_exists(group_id):
        raise PermissionDenied
    group = Groups.objects.get(id=group_id)
    if not isAdmin(request.user, group):
        raise PermissionDenied
    group_name = request.POST.get("group_name", "null")
    group_description = request.POST.get("group_description", "null")
    group_fees = 0
    try:
        group_fees = int(request.POST.get("group_fees", "null"))
    except:
        raise PermissionDenied
    if group_fees < 0:
        raise PermissionDenied

    if group_fees != group.fees:
        transaction_now = Transaction.objects.filter(transaction_user_2=request.user, transaction_group=True, transaction_accepted=False)
        for transaction in transaction_now:
            transaction.transaction_user_1.user_balance += transaction.transaction_amount
            transaction.transaction_user_1.save()
        transaction_now.delete()
        Group_Members.objects.filter(confirmed=False, group_id=group_id).delete()
    group.group_name = group_name
    group.description = group_description
    group.fees = group_fees
    group.save()
    return HttpResponseRedirect(reverse('privacy_settings:group_settings', kwargs={'group_id' : group_id}))

def update_member_deletion_access(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    group_id = request.POST.get("group_id", "null")
    if not group_exists(group_id):
        raise PermissionDenied
    group = Groups.objects.get(id = group_id)
    if not isAdmin(request.user, group):
        raise PermissionDenied
    member_deletion_access = 0
    try:
        member_deletion_access = int(request.POST.get("member_deletion_access", "null"))
    except:
        raise PermissionDenied
    if member_deletion_access not in [0, 1]:
        raise PermissionDenied
    group.member_deletion_access = member_deletion_access
    group.save()
    return HttpResponseRedirect(reverse('privacy_settings:group_settings', kwargs={'group_id': group_id}))

def update_post_view_access(request): # actually it restricts from showing the whole group
    if not request.user.is_authenticated:
        raise PermissionDenied
    group_id = request.POST.get("group_id", "null")
    if not group_exists(group_id):
        raise PermissionDenied
    group = Groups.objects.get(id = group_id)
    if not isAdmin(request.user, group):
        raise PermissionDenied
    post_view_access = 0
    try:
        post_view_access = int(request.POST.get("post_view_access", "null"))
    except:
        raise PermissionDenied
    if post_view_access not in [0, 1]:
        raise PermissionDenied
    group.post_view_access = post_view_access
    group.save()
    return HttpResponseRedirect(reverse('privacy_settings:group_settings', kwargs={'group_id': group_id}))

def send_otp(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if (request.user.user_ongoing_transaction):
        django.contrib.auth.logout(request)
        return HttpResponseRedirect(reverse('logout'))

    request.user.user_ongoing_transaction = True
    # request.user.user_ongoing_transaction = False
    request.user.save()
    otp = getOTP()
    send_mail('SocPay | NoReply', 'Your OTP is : ' + str(otp), 'accounts@socpay.in', [request.user.email],
              fail_silently=False)
    user1 = request.user
    user1.user_last_transaction_for_begin = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    user1.save()
    request.session["otp_verify"] = otp
    request.session['time_add_3'] = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return render(request, 'otp_verify.html')

def verify_otp(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    # print(request.session['user1'], request.session['user2'], request.session['am'], request.session['curr_otp'])

    timenow = datetime.now()
    timethen = datetime.strptime(request.session['time_add_3'],"%d-%b-%Y (%H:%M:%S.%f)")

    if((timenow - timethen).seconds > 60):
        message = 'OTP Timeout'
        d = {}
        request.user.user_ongoing_transaction = False
        request.user.save()
        d['message'] = message
        return render(request, 'display_message_privacy.html', context=d)
        # return HttpResponse("<h1>OTP Timeout<br><a href='wallet_home'>GO BACK</a>")
    entered_otp = request.POST.get("entered_otp", "null")

    timecheck = datetime.strptime(request.user.user_last_transaction_for_otp, "%d-%b-%Y (%H:%M:%S.%f)")

    if ((datetime.now() - timecheck).seconds < 80):
        message = 'Please try after 80 seconds.'
        d = {}
        request.user.user_ongoing_transaction = False
        request.user.save()
        d['message'] = message
        return render(request, 'display_message_privacy.html', context=d)
        # return HttpResponse("<h1>Please try after 80 seconds.<br><a href='wallet_home'>GO BACK</a>")

    try:
        y = int(entered_otp)
    except:
        message = 'OTP Invalid'
        d = {}
        request.user.user_ongoing_transaction = False
        request.user.save()
        d['message'] = message
        return render(request, 'display_message_privacy.html', context=d)
        # return HttpResponse("<h1>OTP Invalid<br><a href='wallet_home'>GO BACK</a>")

    if (int(entered_otp) != int(request.session["otp_verify"])):
        # print(otp1, curr_otp)
        message = 'OTP does not match'
        d = {}
        request.user.user_ongoing_transaction = False
        request.user.save()
        d['message'] = message
        return render(request, 'display_message_privacy.html', context=d)
        # return HttpResponse("<h1>OTP does not match<br><a href='wallet_home'>GO BACK</a>")

    request.user.user_last_transaction_for_otp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    request.user.verified = True
    request.user.user_ongoing_transaction = False
    request.user.save()
    return HttpResponseRedirect(reverse('privacy_settings:settings'))

def update_user_details(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    first_name = request.POST.get("first_name", "null")
    request.user.first_name = first_name
    request.user.save()
    return HttpResponseRedirect(reverse('privacy_settings:settings'))
