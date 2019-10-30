from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import TemplateView

from friends.models import Friend
from main_app.utils import get_friends, get_sent_requests, get_received_requests, get_not_friends
from users.forms import CustomUserCreationForm
from users.models import CustomUser


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('friends:timeline'))
        return super(SignUp, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):


class Friendship(TemplateView):
    template_name = 'friends.html'

    # def get(self, request, *args, **kwargs):
    #     if request.method == "Post":
    #         if request.POST.get("no_friends"):
    #             friend_name = request.POST.get('friends', 'default')
    #             print(friend_name)
    #     return HttpResponseRedirect(reverse('friends', args=[request.user.username]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends_list'] = get_friends(self.request.user)
        context['requests_sent'] = get_sent_requests(self.request.user)
        context['requests_received'] = get_received_requests(self.request.user)
        context['not_friends'] = get_not_friends(context['friends_list'], context['requests_sent'], context['requests_received'])
        #print(context['friends_list'])
        # for friend in context['friends_list']:
            #print(friend)
        # print()
        # for friend in context['requests_sent']:
        #     print(friend)
        # # print()
        # for friend in context['requests_received']:
        #     print(friend)
        # # print()
        # for friend in context['not_friends']:
        #     print(friend)
        return context


def add_friend(request):
    # print(request.user.id)
    if not request.user.is_authenticated:
        raise PermissionDenied
    friend_id = request.POST.get('friend', 'default')
    if not CustomUser.objects.filter(id=friend_id).exists():
        raise SuspiciousOperation("Please be in limits.")
    obj1 = list(Friend.objects.filter(creator_id=request.user.id, follower_id = friend_id))
    obj2 = list(Friend.objects.filter(follower_id=request.user.id, creator_id=friend_id))
    if len(obj1) == 0 and len(obj2) == 0:
        Friend.objects.create(creator_id=request.user.id, follower_id=friend_id, confirmed=False)

    return HttpResponseRedirect(reverse('friends:friends'))


def decline(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    friend_id = request.POST.get('friend', 'default')
    # print(friend)
    if not CustomUser.objects.filter(id=friend_id).exists():
        raise SuspiciousOperation("Please be in limits.")
    Friend.objects.filter(creator_id=friend_id, follower_id=request.user.id, confirmed=False).delete()
    return HttpResponseRedirect(reverse('friends:friends'))


def accept(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    # print("hiiiiiiii")
    friend_id = request.POST.get('friend', 'default')
    if not CustomUser.objects.filter(id=friend_id).exists():
        raise SuspiciousOperation("Please be in limits.")
    row = Friend.objects.get(creator_id=friend_id, follower_id=request.user.id, confirmed=False)
    row.confirmed = True
    row.save()
    # print("hi")
    # print(Friend.objects.get(creator_id=friend_id,follower_id=request.user.id).confirmed)
    return HttpResponseRedirect(reverse('friends:friends'))


def cancel(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    friend_id = request.POST.get('friend', 'default')
    if not CustomUser.objects.filter(id=friend_id).exists():
        raise SuspiciousOperation("Please be in limits.")
    Friend.objects.filter(creator_id=request.user.id, follower_id=friend_id).delete()
    return HttpResponseRedirect(reverse('friends:friends'))


def remove_friend(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    friend_id = request.POST.get('friend', 'default')
    if not CustomUser.objects.filter(id=friend_id).exists():
        raise SuspiciousOperation("Please be in limits.")
    row = Friend.objects.filter(creator_id=request.user.id, follower_id=friend_id)
    # print("ro")
    # print(row)
    if not row:
        row = Friend.objects.filter(creator_id=friend_id, follower_id=request.user.id)
    # print(row)
    row[0].delete()
    return HttpResponseRedirect(reverse('friends:friends'))

def check_signup_request(request):
    """Checks if the user is already logged in"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('friends:timeline'))
    print(request.POST.get("date_of_birth", "null"))

    return HttpResponseRedirect(reverse('users:signup'))

# def password_reset_custom(request):
#     return password_reset