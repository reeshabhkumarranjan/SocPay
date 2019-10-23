from users.models import Friend, CustomUser


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
    return friend_arr


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
        if i not in friends and i not in requests_received and i not in requests_sent:
            not_friends.append(i)
    return not_friends