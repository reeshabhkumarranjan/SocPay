from django.shortcuts import render
from main_app.utils import get_friends
from private_message.models import getAllMessages
from users.models import CustomUser
# Create your views here.

def friends_message(request):
    my_friends = get_friends(request.user)
    context = {'my_friends': my_friends}
    return render(request, 'private_message.html', context)

def chat(request):
    user1 = request.user
    user2_id = request.POST.get("user_id")
    user2 = CustomUser.objects.get(id=user2_id)
    messages = getAllMessages(user1, user2)
    context = {"messages": messages}
    return render(request, 'chat.html', context)