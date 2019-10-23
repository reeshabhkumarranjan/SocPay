import pyotp as pyotp
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
from main_app.models import Post, Transaction
from users.models import Friend, CustomUser


def register(request):
    """This just displays the register page."""
    return render(request, 'signup.html')


def login(request):
    """This just displays the register page."""
    if request.user.is_authenticated():
        return redirect('main_app:timeline')
    return render(request, 'registration/login.html')


def index(request):
    return render(request, 'index.html')

def timeline(request):
    all_posts = Post.objects.filter(recipient_name=request.user.username).order_by('-post_date')
    context = {'forloop' : range(100), 'all_posts' : all_posts}
    return render(request, 'timeline.html', context=context)

def friends(request):
    if request.method == 'POST':
        pass # TODO complete this
    # all_friends = Friend.objects.all(creator__id=)
    all_friends = (Friend.objects.filter(creator=request.user) | Friend.objects.filter(follower=request.user)) & Friend.objects.filter(confirmed=True)
    all_strangers = CustomUser.objects.all()
    context = {'all_friends' : all_friends, 'all_strangers' : all_strangers}
    return render(request, 'friends.html', context=context)

def add_post(request):
    # TODO add checks
    author_name = request.user.username
    recipient_name = request.user.username
    post_text = request.POST.get('post_text', "N/A")

    Post.objects.create(author_name=author_name, recipient_name=recipient_name, post_text=post_text)
    return redirect('main_app:timeline')

def add_post_friend(request, friend_username):
    # TODO add checks
    author_name = request.user.username
    recipient_name = friend_username
    post_text = request.POST.get('post_text', "N/A")

    Post.objects.create(author_name=author_name, recipient_name=recipient_name, post_text=post_text)
    return redirect('main_app:friend_timeline', friend_username=friend_username)
    # return redirect('https://google.com')

def friend_timeline(request, friend_username):
    all_posts = Post.objects.filter(recipient_name=friend_username).order_by('-post_date')
    context = {'friend_username' : friend_username, 'all_posts' : all_posts}
    return render(request, 'friend_timeline.html', context=context)

# wallet

def transfer_money(request):
    all_users = CustomUser.objects.all()
    context = {'all_users' : all_users}
    return render(request, 'transfer_money.html', context=context)

def wallet_home(request):
    user1 = request.user
    d = {'name':user1.username, 'bal':user1.user_balance, 'trans':user1.user_no_of_transactions}
    return render(request, 'wallet.html', context=d)
    # return HttpResponse("<h1>HERE</h1>")
def transactions(request):
    user1 = request.user
    d={'name':user1.user_transactions_list}
    return render(request, 'transactions.html', d)

def transfer(request):

    u2 = 0
    am = 0

    try:
        u2 = str(request.GET.get('to'))
        am = int(request.GET.get('amount'))
    except:
        return HttpResponse("<h1>Please enter valid values<br><a href='http://google.com'>GO BACK</a>")

    if(am<=0):
        return HttpResponse("<h1>Positive value required<br><a href='http://google.com'>GO BACK</a>")

    user1 = request.user
    user2 = 0
    try:
        user2 = CustomUser.objects.get(username = u2)
    except:
        return HttpResponse("<h1>User Not Found<br><a href='http://google.com'>GO BACK</a>")

    if (user1.user_no_of_transactions + 1 > user1.user_no_of_transactions_allowed): # MAX LIMIT ----> CHANGE
        return HttpResponse(
            "<h1>You have reached max. transaction limit<br><a href='http://google.com'>GO BACK</a>")

    if(am > user1.user_balance):
        return HttpResponse("<h1>Insufficient Balance to transfer entered amount<br><a href='http://google.com'>GO BACK</a>")

    totp = pyotp.TOTP('base32secret3232')
    curr_otp = totp.now()

    request.session['user1'] = user1.username
    request.session['user2'] = user2.username
    request.session['am'] = str(am)
    request.session['curr_otp'] = str(curr_otp)

    print(curr_otp)

    return render(request, 'otp.html')



def make_changes(request):

    print(request.session['user1'], request.session['user2'], request.session['am'],request.session['curr_otp'] )

    user1 = CustomUser.objects.get(username = request.session['user1'])
    user2 = CustomUser.objects.get(username = request.session['user2'])
    am = int(request.session['am'])
    curr_otp = request.session['curr_otp']

    otp1 = str(request.GET.get('otp'))

    print(otp1,curr_otp)

    if(int(otp1) != int(curr_otp)):
        print(otp1, curr_otp)
        return HttpResponse("<h1>OTP does not match<br><a href='http://google.com'>GO BACK</a>")

    # user1 = 0
    # user2 = 0

    user1.user_balance -= am;
    user2.user_balance += am;

    user1.user_no_of_transactions += 1;

    dt = datetime.now()

    Transaction.objects.create(transaction_user_1 = user1, transaction_user_2 = user2, transaction_amount = am, transaction_date = dt, transaction_time = dt)
    tempS = "from : "+str(user1.username)+"  "+"to : "+str(user2.username)+"  "+"amount : "+str(am)+"  "+"date & time : "+str(dt)
    user1.user_transactions_list+=tempS+'\n'
    user2.user_transactions_list+=tempS+'\n'

    user1.save()
    user2.save()

    return HttpResponse("<h1>Money Transeferred Successfully<br><a href='http://google.com'>GO BACK</a>")
