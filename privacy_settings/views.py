from datetime import datetime, timedelta

from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from groups.models import Groups
from main_app import utils
from users.models import CustomUser
from wallet.utils import execute_transaction, getOTP


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
    if user_type == 5 and not request.user.verified:
        return utils.raise_exception(request, "You need to be verified to upgrade to a commercial user.")
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

def send_otp(request):

    otp = getOTP()
    send_mail('SocPay | NoReply', 'Your OTP is : ' + str(otp), 'accounts@socpay.in', [request.user.email],
              fail_silently=False)
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
        return HttpResponse("<h1>Session Timeout<br><a href='wallet_home'>GO BACK</a>")
    entered_otp = request.POST.get("entered_otp", "null")

    timecheck = datetime.strptime(request.user.user_last_transaction_for_otp, "%d-%b-%Y (%H:%M:%S.%f)")

    if ((datetime.now() - timecheck).seconds < 80):
        return HttpResponse("<h1>Please try after 80 seconds.<br><a href='wallet_home'>GO BACK</a>")

    try:
        y = int(entered_otp)
    except:
        return HttpResponse("<h1>OTP Invalid<br><a href='wallet_home'>GO BACK</a>")

    if (int(entered_otp) != int(request.session["otp_verify"])):
        # print(otp1, curr_otp)
        return HttpResponse("<h1>OTP does not match<br><a href='wallet_home'>GO BACK</a>")

    request.user.user_last_transaction_for_otp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    request.user.verified = True
    request.user.save()
    return HttpResponseRedirect(reverse('privacy_settings:settings'))
