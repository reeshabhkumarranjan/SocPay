import pyotp
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from main_app import utils
from main_app.utils import get_friends, are_friend
from users.models import CustomUser
# from wallet.forms import transaction_form
from wallet.models import Transaction
from datetime import datetime
from .utils import getOTP
import django


def wallet_home(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    user1 = request.user
    d = {'name': user1.username, 'bal': user1.user_balance, 'trans': user1.user_no_of_transactions}
    return render(request, 'wallet.html', context=d)


def transactions_to_be_accepted(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    user1 = request.user
    # print('I AM HERE')
    trans_list = []
    trans_list = Transaction.objects.filter(transaction_accepted=False) & Transaction.objects.filter(
        transaction_user_2=user1)
    d = {}
    d['transactions'] = trans_list

    return render(request, 'transactions_list.html', context=d)


def transactions_completed(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    user1 = request.user
    # print('I AM HERE')
    trans_list = []
    trans_list = Transaction.objects.filter(transaction_accepted=True) & (
                Transaction.objects.filter(transaction_user_2=user1) | Transaction.objects.filter(
            transaction_user_1=user1))
    d = {}
    d['trans_list'] = trans_list

    return render(request, 'transactions_completed.html', context=d)


def transactions_pending(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
        raise PermissionDenied
    user1 = request.user
    # print('I AM HERE')
    trans_list = []
    trans_list = Transaction.objects.filter(transaction_accepted=False) & Transaction.objects.filter(
        transaction_user_1=user1)
    d = {}
    d['trans_list'] = trans_list

    return render(request, 'transactions_pending.html', context=d)


def transfer(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.method == 'POST':

        if (request.user.user_ongoing_transaction):
            django.contrib.auth.logout(request)
            return HttpResponseRedirect(reverse('logout'))

        request.user.user_ongoing_transaction = True
        # request.user.user_ongoing_transaction = False
        request.user.save()

        user2_username = request.POST.get("username", "null")
        user2 = CustomUser.objects.get(username=user2_username)
        amount = 0
        try:
            amount = int(request.POST.get("amount", "null"))
        except:
            message = 'Please enter valid input.'
            d = {}
            d['message'] = message
            request.user.user_ongoing_transaction = False
            request.user.save()
            return render(request, 'display_message_1.html', context=d)

        if(user2.username=='admin'):
            message = 'You Cannot Send Money To Admin'
            d = {}
            d['message'] = message
            request.user.user_ongoing_transaction = False
            request.user.save()
            return render(request, 'display_message_1.html', context=d)
            # return HttpResponse('''<h1>You Cannot Send Money To Admin<br><a href="wallet_home">GO BACK</a>''')

        user1 = request.user

        # print(request.user.user_last_transaction)
        # print((datetime.now() - timecheck).seconds)

        am = amount

        if (am <= 0):
            message = 'Positive value required'
            d = {}
            d['message'] = message
            request.user.user_ongoing_transaction = False
            request.user.save()
            return render(request, 'display_message_1.html', context=d)
            # return HttpResponse('''<h1>Positive value required<br><a href="wallet_home">GO BACK</a>''')

        if user1.user_type != 5 and not are_friend(user1, user2):
            return utils.raise_exception(request, "Become a commercial user to send money to strangers.")

        if (user1.username == user2.username):
            message = 'You cannot transfer money to yourself'
            d = {}
            d['message'] = message
            request.user.user_ongoing_transaction = False
            request.user.save()
            return render(request, 'display_message_1.html', context=d)
            # return HttpResponse(
                # "<h1>You cannot transfer money to yourself<br><a href='wallet_home'>GO BACK</a>")

        if user1.user_no_of_transactions + 1 > user1.user_no_of_transactions_allowed:  # MAX LIMIT ----> CHANGE
            message = 'You have reached max. transaction limit'
            d = {}
            d['message'] = message
            request.user.user_ongoing_transaction = False
            request.user.save()
            return render(request, 'display_message_1.html', context=d)
            # return HttpResponse(
            #     "<h1>You have reached max. transaction limit<br><a href='wallet_home'>GO BACK</a>")

        if (am > user1.user_balance):
            message = 'Insufficient Balance to transfer entered amount'
            d = {}
            d['message'] = message
            request.user.user_ongoing_transaction = False
            request.user.save()
            return render(request, 'display_message_1.html', context=d)
            # return HttpResponse(
            #     "<h1>Insufficient Balance to transfer entered amount<br><a href='wallet_home'>GO BACK</a>")

        timecheck = datetime.strptime(user1.user_last_transaction_for_begin, "%d-%b-%Y (%H:%M:%S.%f)")

        if ((datetime.now() - timecheck).seconds < 80):
            message = 'Try after 80 seconds'
            d = {}
            d['message'] = message
            request.user.user_ongoing_transaction = False
            request.user.save()
            return render(request, 'display_message_1.html', context=d)
            # return HttpResponse("<h1>Try after 80 seconds<br><a href='wallet_home'>GO BACK</a>")


        user1.user_last_transaction_for_begin = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

        user1.save()

        # totp = pyotp.TOTP('base32secret3232')
        curr_otp = getOTP()


        # request.session['date_time'] = str(datetime.datet)

        # print(curr_otp)
        # print(curr_otp)
        send_mail('SocPay | NoReply', 'Your OTP is : ' + str(curr_otp), 'accounts@socpay.in', [user1.email], fail_silently=False)

        request.session['user1'] = user1.username
        request.session['user2'] = user2.username
        request.session['am'] = str(am)
        request.session['curr_otp'] = str(curr_otp)
        request.session['time'] = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

        return render(request, 'otp_tranfer.html')

            # return HttpResponseRedirect('/thanks/')
    else:
        all_friends = get_friends(request.user)
        if (request.user.user_ongoing_transaction):
            django.contrib.auth.logout(request)
            return HttpResponseRedirect(reverse('logout'))
        else:
            request.user.user_ongoing_transaction = True
            request.user.save()
        if request.user.user_type == 5:
            all_friends = CustomUser.objects.filter(~Q(username="admin")) & CustomUser.objects.filter(~Q(username=request.user.username))
        context = {'all_friends':all_friends}
        return render(request, 'transfer_money.html', context=context)
        # form = transaction_form(request.user)

        # print(form)


    # u2 = 0
    # am = 0
    #
    # form  =
    # try:
    #     u2 = str(request.GET.get('to'))
    #     am = int(request.GET.get('amount'))
    # except:
    #     return HttpResponse("<h1>Please enter valid values<br><a href='http://google.com'>GO BACK</a>")


def make_changes(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    # print(request.session['user1'], request.session['user2'], request.session['am'], request.session['curr_otp'])

    timenow = datetime.now()
    timethen = datetime.strptime(request.session['time'],"%d-%b-%Y (%H:%M:%S.%f)")

    if((timenow - timethen).seconds > 60):
        message = 'Session Timeout'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse("<h1>Session Timeout<br><a href='wallet_home'>GO BACK</a>")

    user1 = CustomUser.objects.get(username=request.session['user1'])

    timecheck = datetime.strptime(user1.user_last_transaction_for_otp, "%d-%b-%Y (%H:%M:%S.%f)")

    if ((datetime.now() - timecheck).seconds < 80):
        message = 'Please try after 80 seconds.'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse("<h1>Please try after 80 seconds.<br><a href='wallet_home'>GO BACK</a>")

    # timecheck = datetime.strptime(user1.user_last_transaction,"%d-%b-%Y (%H:%M:%S.%f)")

    # if((datetime.now() - timecheck).seconds < 76):
    #     return HttpResponse("<h1>Something Went Wrong<br><a href='http://google.com'>GO BACK</a>")

    user2 = CustomUser.objects.get(username=request.session['user2'])
    am = int(request.session['am'])
    curr_otp = request.session['curr_otp']

    otp1 = str(request.POST.get('otp'))

    # print(otp1,curr_otp)

    try:
        y = int(otp1)
    except:
        message = 'OTP invalid'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse("<h1>OTP invalid<br><a href='wallet_home'>GO BACK</a>")

    if (int(otp1) != int(curr_otp)):
        # print(otp1, curr_otp)
        message = 'OTP does not match'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse("<h1>OTP does not match<br><a href='wallet_home'>GO BACK</a>")

    # user1 = 0
    # user2 = 0

    user1.user_balance -= am;
    # user2.user_balance += am;

    user1.user_no_of_transactions += 1;

    dt = datetime.now()

    Transaction.objects.create(transaction_user_1=user1, transaction_user_2=user2, transaction_amount=am,
                               transaction_date=dt, transaction_time=dt, transaction_accepted=False)
    # tempS = "from : "+str(user1.username)+"  "+"to : "+str(user2.username)+"  "+"amount : "+str(am)+"  "+"date & time : "+str(dt)
    # user1.user_transactions_list+=tempS+'\n'
    # user2.user_transactions_list+=tempS+'\n'

    user1.user_last_transaction_for_otp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    user1.user_ongoing_transaction = False
    user1.save()
    user2.save()

    message = 'Money Requested Successfully'
    d = {}
    d['message'] = message
    return render(request, 'display_message_1.html', context=d)

    # return HttpResponse("<h1>Money Requested Successfully<br><a href='wallet_home'>GO BACK</a>")


def add_money(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    return render(request, 'add_money.html')


def add_money_work(request):
    if not request.user.is_authenticated:
        raise PermissionDenied


    user1 = request.user
    amount = 0
    try:
        amount = float(request.POST.get('amount'))

        amount = int(amount)
    except:
        message = 'Enter Valid Value'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse('''<h1>Value >=1 Required<br><a href="wallet_home">GO BACK</a>''')

    if (amount <= 0):
        message = 'Value >1 Required'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse('''<h1>Value >1 Required<br><a href="wallet_home">GO BACK</a>''')

    if user1.user_no_of_transactions + 1 > user1.user_no_of_transactions_allowed:  # MAX LIMIT ----> CHANGE
        message = 'You have reached max. transaction limit'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse(
        #     "<h1>You have reached max. transaction limit<br><a href='wallet_home'>GO BACK</a>")

    timecheck = datetime.strptime(user1.user_last_transaction_for_begin, "%d-%b-%Y (%H:%M:%S.%f)")

    if ((datetime.now() - timecheck).seconds < 80):
        message = 'Please try after 80 seconds'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse("<h1>Please try after 80 seconds<br><a href='wallet_home'>GO BACK</a>")

    # user1 = request.user
    # user1.user_balance += amount
    # user1.save()

    user1.user_last_transaction_for_begin = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

    user1.save()

    # totp = pyotp.TOTP('base32secret3232')
    curr_otp = getOTP()

    # request.session['date_time'] = str(datetime.datet)

    # print(curr_otp)
    # print(curr_otp)
    send_mail('SocPay | NoReply', 'Your OTP is : ' + str(curr_otp), 'accounts@socpay.in', [user1.email],
              fail_silently=False)

    request.session['user1_add'] = user1.username
    request.session['user2_add'] = 'admin'
    request.session['am_add'] = str(amount)
    request.session['curr_otp_add'] = str(curr_otp)
    request.session['time_add'] = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

    return render(request, 'otp_add_money.html')

    # return HttpResponse("<h1>Money Transeferred Successfully<br><a href='wallet_home'>GO BACK</a>")

def add_money_after_otp(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    # print(request.session['user1'], request.session['user2'], request.session['am'], request.session['curr_otp'])

    timenow = datetime.now()
    timethen = datetime.strptime(request.session['time_add'],"%d-%b-%Y (%H:%M:%S.%f)")

    if((timenow - timethen).seconds > 60):
        message = 'Session Timeout'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse("<h1>Session Timeout<br><a href='wallet_home'>GO BACK</a>")

    user1 = CustomUser.objects.get(username=request.session['user1_add'])

    timecheck = datetime.strptime(user1.user_last_transaction_for_otp, "%d-%b-%Y (%H:%M:%S.%f)")

    if ((datetime.now() - timecheck).seconds < 80):
        message = 'Please try after 80 seconds.'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse("<h1>Please try after 80 seconds.<br><a href='wallet_home'>GO BACK</a>")

    user2 = CustomUser.objects.get(username=request.session['user2_add'])
    am = int(request.session['am_add'])
    curr_otp = request.session['curr_otp_add']

    otp1 = str(request.POST.get('otp'))

    # print(otp1,curr_otp)

    try:
        y = int(otp1)
    except:
        message = 'OTP Invalid'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse("<h1>OTP Invalid<br><a href='wallet_home'>GO BACK</a>")

    if (int(otp1) != int(curr_otp)):
        message = 'OTP does not match'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # print(otp1, curr_otp)
        # return HttpResponse("<h1>OTP does not match<br><a href='wallet_home'>GO BACK</a>")

    # user1.user_balance += am;
    # user2.user_balance += am;

    # user1.user_no_of_transactions += 1;

    dt = datetime.now()

    Transaction.objects.create(transaction_user_1=user1, transaction_user_2=user2, transaction_amount=am,
                               transaction_date=dt, transaction_time=dt, transaction_accepted=False, transaction_money_add=True)
    # tempS = "from : "+str(user1.username)+"  "+"to : "+str(user2.username)+"  "+"amount : "+str(am)+"  "+"date & time : "+str(dt)
    # user1.user_transactions_list+=tempS+'\n'
    # user2.user_transactions_list+=tempS+'\n'

    user1.user_last_transaction_for_otp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

    user1.save()
    user2.save()

    message = 'Money Will be Added Shortly'
    d = {}
    d['message'] = message
    return render(request, 'display_message_1.html', context=d)
    # return HttpResponse("<h1>Money Will be Added Shortly<br><a href='wallet_home'>GO BACK</a>")



def transaction_accept(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    id = -1
    try:
        id = int(request.POST.get('transaction_id'))
    except:
        message = '404 not found'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse("<h1>404 not found<br><a href='wallet_home'>GO BACK</a>")

    if(request.user.username == 'admin'):
        transaction_now = Transaction.objects.get(pk=id)
        transaction_now.transaction_accepted = True
        transaction_now.save()
        sender = CustomUser.objects.get(username=transaction_now.transaction_user_1.username)
        sender.user_balance += transaction_now.transaction_amount
        sender.save()
        return HttpResponseRedirect('transactions_to_be_accepted')

    transaction_now = Transaction.objects.get(pk=id)
    transaction_now.transaction_accepted = True
    # Transaction.objects.filter(pk=id).update(transaction_accept=)
    sender = CustomUser.objects.get(username=transaction_now.transaction_user_1.username)
    receiver = CustomUser.objects.get(username=transaction_now.transaction_user_2.username)

    receiver.user_balance += transaction_now.transaction_amount

    transaction_now.save()
    sender.save()
    receiver.save()
    # return transactions(request)
    return HttpResponseRedirect('transactions_to_be_accepted')


def transaction_decline(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    id = -1
    try:
        id = int(request.POST.get('transaction_id'))
    except:
        message = '404 not found'
        d = {}
        d['message'] = message
        return render(request, 'display_message_1.html', context=d)
        # return HttpResponse("<h1>404 not found<br><a href='wallet_home'>GO BACK</a>")

    if (request.user.username == 'admin'):
        transaction_now = Transaction.objects.get(pk=id)
        transaction_now.transaction_accepted = False
        transaction_now.delete()
        return HttpResponseRedirect('transactions_to_be_accepted')

    transaction_now = Transaction.objects.get(id=id)
    transaction_now.transaction_accepted = False
    sender = CustomUser.objects.get(username=transaction_now.transaction_user_1.username)
    receiver = CustomUser.objects.get(username=transaction_now.transaction_user_2.username)

    sender.user_balance += transaction_now.transaction_amount
    sender.user_no_of_transactions -= 1

    transaction_now.delete()

    sender.save()
    receiver.save()
    return HttpResponseRedirect('transactions_to_be_accepted')


def transfer_money(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    all_users = CustomUser.objects.all()  # TODO fix database query
    context = {'all_users': all_users}
    return render(request, 'transfer_money.html', context=context)

