from datetime import datetime

from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from friends.models import Friend
from main_app import utils
from main_app.models import Post
from main_app.utils import are_friend
from users.models import CustomUser
from django.contrib.auth.signals import user_logged_in

# def initialise_user(sender, user, request, **kwargs):
#     request.user.user_ongoing_transaction = False
#     print("initialising user", str(request.user.user_ongoing_transaction))
#     request.user.save()

def username_exists(username):
    user = None
    try:
        user = CustomUser.objects.get(username=username)
    except:
        return False
    return True

def timeline(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    # user_logged_in.connect(initialise_user)
    if request.user.expiration_date < datetime.now():
        request.user.user_type = 1
        request.user.expiration_date = datetime.now()
    if (str(request.session.session_key) != request.user.user_last_session):
        request.user.user_ongoing_transaction = False
        request.user.user_last_session = str(request.session.session_key)
    # print(request.user.user_ongoing_transaction)
    request.user.save()
    all_posts = Post.objects.filter(recipient_name=request.user.username).order_by('-post_date')
    context = {'forloop' : range(100), 'all_posts' : all_posts}
    return render(request, 'timeline.html', context=context)

def friends(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    query = None
    filter = False
    if request.method == 'POST':
        query = request.POST.get("query", "null")
        filter = True
    all_friends = utils.get_friends(request.user)
    all_strangers = utils.get_not_friends(request.user)
    all_requests_sent = utils.get_sent_requests(request.user)
    all_requests_received = utils.get_received_requests(request.user)
    search_hint = 'null'
    if filter:
        all_friends = utils.search_users(all_friends, query)
        all_strangers = utils.search_users(all_strangers, query)
        all_requests_sent = utils.search_users(all_requests_sent, query)
        all_requests_received = utils.search_users(all_requests_received, query)
        search_hint = query
    # all_friends = Friend.objects.all(creator__id=)
    context = {'all_friends' : all_friends, 'all_strangers' : all_strangers, 'all_requests_sent' : all_requests_sent, 'all_requests_received' : all_requests_received, 'search_hint' : search_hint}
    return render(request, 'friends.html', context=context)

def add_post(request):
    # TODO add checks
    if not request.user.is_authenticated:
        raise PermissionDenied
    author_name = request.user.username
    recipient_name = request.user.username
    post_text = request.POST.get('post_text', "N/A")

    utils.check_captcha(request)

    Post.objects.create(author_name=author_name, recipient_name=recipient_name, post_text=post_text)
    return redirect('friends:timeline')

def add_post_friend(request, friend_username):
    # TODO add checks
    if not request.user.is_authenticated:
        raise PermissionDenied
    # friend = None
    # try:
    #     friend = CustomUser.objects.get(username=friend_username)
    # except:
    #     raise PermissionDenied
    utils.check_captcha(request)
    if not username_exists(friend_username):
        raise PermissionDenied
    friend = CustomUser.objects.get(username=friend_username)
    if not are_friend(request.user, friend):
        raise PermissionDenied
    author_name = request.user.username
    recipient_name = friend_username
    post_text = request.POST.get('post_text', "N/A")

    Post.objects.create(author_name=author_name, recipient_name=recipient_name, post_text=post_text)
    return redirect('friends:friend_timeline', friend_username=friend_username)
    # return redirect('https://google.com')

def friend_timeline(request, friend_username):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if not username_exists(friend_username):
        raise PermissionDenied
    if request.user.username == friend_username:
        return HttpResponseRedirect(reverse('friends:timeline'))
    friend = CustomUser.objects.get(username=friend_username)
    if not are_friend(request.user, friend) and friend.timeline_view_level == 0:
        return utils.raise_exception(request, "You are not allowed to view the timeline.")
    all_posts = Post.objects.filter(recipient_name=friend_username).order_by('-post_date')
    can_post = (friend.timeline_post_level == 1) or are_friend(request.user, friend)
    context = {'friend_username' : friend_username, 'all_posts' : all_posts, 'can_post' : can_post}
    return render(request, 'friend_timeline.html', context=context)
