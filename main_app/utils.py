from django.shortcuts import render

from friends.models import Friend
from users.models import CustomUser
from wallet.models import Transaction

def search_users(_list, query):
    if query != None:
        if query == "":
            return _list
        friend_arr_query = []
        for i in range(len(_list)):
            if _list[i].first_name.lower()[:len(query)] == str(query).lower() or _list[i].username.lower()[:len(query)] == str(query).lower():
                friend_arr_query.append(_list[i])
        return friend_arr_query

def search_groups(_list, query):
    if query != None:
        if query == "":
            return _list
        group_arr_query = []
        for i in range(len(_list)):
            if _list[i].group_name.lower()[:len(query)] == str(query).lower():
                group_arr_query.append(_list[i])
        return group_arr_query



def get_friends(user):
    # print("nikal")
    barr = Friend.objects.all();
    # print(barr)
    # print(user)
    arr = Friend.objects.filter(creator=user, confirmed=True).values_list("follower")
    arr1 = Friend.objects.filter(follower=user, confirmed=True).values_list("creator")
    friend_arr = []
    # print(arr)
    # print(arr1)
    for i in arr:
        # print(type(i[0]))
        friend_arr.append(CustomUser.objects.get(pk=i[0]))
    for i in arr1:
        friend_arr.append(CustomUser.objects.get(pk=i[0]))
    # friend_arr.remove(user)
    id_list = [friend.id for friend in friend_arr]
    friend_arr = CustomUser.objects.filter(pk__in=id_list)
    return friend_arr

def get_chat_friends(user):
    pass


def get_received_requests(user):
    arr = Friend.objects.filter(follower=user, confirmed=False).values_list("creator")
    friend_arr = []
    for i in arr:
        friend_arr.append(CustomUser.objects.get(id=i[0]))
    return friend_arr


def get_sent_requests(user):
    arr = Friend.objects.filter(creator=user, confirmed=False).values_list("follower")
    friend_arr = []
    for i in arr:
        friend_arr.append(CustomUser.objects.get(id=i[0]))
    return friend_arr


def get_not_friends(user):
    friends = get_friends(user)
    requests_sent = get_sent_requests(user)
    requests_received = get_received_requests(user)
    arr = CustomUser.objects.all()
    not_friends = []
    for i in arr:
        if i not in friends and i not in requests_received and i not in requests_sent and i != user:
            not_friends.append(i)
    return not_friends

def get_transactions(user):
    list = Transaction.objects.filter(transaction_user2=user)
    return list

def raise_exception(request, error_message):
    return render(request, 'exception_message.html', context={'error_message':error_message})

def are_friend(user1, user2):
    friends = get_friends(user1)
    return user2 in friends