from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from main_app import utils
from main_app.utils import get_friends, get_chat_friends, get_chat_friends_for_commercial, are_friend
from private_message.models import getAllMessages, Private_Message
from users.models import CustomUser
# Create your views here.

def friends_message(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    # if request.user.user_type == 1:
    #     return utils.raise_exception(request, "Upgrade your account to chat with other users.")
    # my_friends = get_friends(request.user)
    my_friends = get_chat_friends(request.user)
    if request.user.user_type == 5:
        my_friends = get_chat_friends_for_commercial(request.user)
    context = {'my_friends': my_friends}
    context['display_message_box'] = False
    if request.method=='POST':
        friend_username = request.POST.get("friend_username", "null")
        friend_user = CustomUser.objects.get(username=friend_username)

        # if request.POST.get("button_clicked", "null") == "send_message":
        #     message_text = request.POST.get("message_text", "null")
        #     Private_Message.objects.create(sender=request.user, receiver=friend_user, message=message_text)

        context['friend_username'] = friend_username
        context['chats'] = getAllMessages(user1=request.user, user2=friend_user)
        context['display_message_box'] = True

    return render(request, 'private_message.html', context)

def friends_message_username(request, friend_username):
    if not request.user.is_authenticated:
        raise PermissionDenied
    # if request.user.user_type == 1:
    #     raise PermissionDenied
    # my_friends = get_friends(request.user)
    my_friends = get_chat_friends(request.user)
    if request.user.user_type == 5:
        my_friends = get_chat_friends_for_commercial(request.user)
    friend_user = CustomUser.objects.get(username=friend_username)
    context = {'my_friends': my_friends}
    context['display_message_box'] = True
    context['friend_username'] = friend_username
    context['chats'] = getAllMessages(user1=request.user, user2=friend_user)

    if request.method=='POST':
        friend_username = request.POST.get("friend_username", "null")
        friend_user = CustomUser.objects.get(username=friend_username)

        # if request.POST.get("button_clicked", "null") == "send_message":
        #     message_text = request.POST.get("message_text", "null")
        #     Private_Message.objects.create(sender=request.user, receiver=friend_user, message=message_text)

        context['friend_username'] = friend_username
        context['chats'] = getAllMessages(user1=request.user, user2=friend_user)
        context['display_message_box'] = True

    return render(request, 'private_message.html', context)

def send_message(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.user.user_type == 1:
        return utils.raise_exception(request, "Upgrade your account to send messages.")

    friend_username = request.POST.get('friend_username', 'null')
    friend_user = CustomUser.objects.get(username=friend_username)
    if request.user.user_type != 5 and not are_friend(request.user, friend_user):
        return utils.raise_exception(request, "You are not allowed to send messages to strangers.")
    message_text = request.POST.get("message_text", "null")
    my_friends = get_friends(request.user)
    Private_Message.objects.create(sender=request.user, receiver=friend_user, message=message_text)
    context = {'my_friends': my_friends}
    context['chats'] = getAllMessages(user1=request.user, user2=friend_user)
    context['friend_username'] =friend_username
    context['display_message_box'] = True
    return HttpResponseRedirect(reverse('private_message:friends_message_username', kwargs={'friend_username' : friend_username}))
    # return render(request, 'private_message.html', context)

def chat(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    user1 = request.user
    user2_id = request.POST.get("user_id")
    user2 = CustomUser.objects.get(id=user2_id)
    messages = getAllMessages(user1, user2)
    context = {"messages": messages}
    return render(request, 'chat.html', context)