from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from groups.models import Groups, giveMyGroups, getOwnedGroups, giveGroupMembers, giveOtherGroups, Group_Members, \
    getMyPendingRequests, getPendingRequests, Group_Posts, getGroupPosts
from main_app import utils
from users.models import CustomUser
from .forms import GroupCreateForm
from django.core.mail import send_mail

def showMyGroups(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.user.user_type == 1:
        raise PermissionDenied

    query = None
    filter = False
    search_hint = ''
    if request.method == 'POST':
        query = request.POST.get("query", "null")
        filter = True
    context = {}
    # context['my_groups'] = list(getOwnedGroups(request.user))
    my_groups = getOwnedGroups(request.user)
    incoming_requests = []
    for group in my_groups:
        incoming_requests += (getPendingRequests(group))
    # print(context['my_groups'])
    search_hint = 'null'
    if filter:
        # incoming_requests = utils.search_groups(incoming_requests, query)
        my_groups = utils.search_groups(my_groups, query)
        search_hint = query
    context['incoming_requests'] = incoming_requests
    context['my_groups'] = my_groups
    context['search_hint'] = search_hint
    return render(request, 'admin_groups.html', context=context)

def show_groups(request):
    filter = False
    query = None
    if request.method == "POST":
        filter = True
        query = request.POST.get("query", "null")
    context = {}
    member_groups = giveMyGroups(request.user)
    other_groups = giveOtherGroups(request.user, member_groups)
    sent_requests = getMyPendingRequests(request.user)
    search_hint = 'null'
    if filter:
        member_groups = utils.search_groups(member_groups, query)
        other_groups = utils.search_groups(other_groups, query)
        sent_requests = utils.search_groups(sent_requests, query)
        search_hint = query

    context['search_hint'] = search_hint
    context['member_groups'] = member_groups
    context['other_groups'] = other_groups
    context['sent_requests'] = sent_requests

    return render(request, 'groups.html', context=context)

class ShowGroups(TemplateView):
    template_name = 'groups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_groups'] = giveMyGroups(self.request.user)
        context['other_groups'] = giveOtherGroups(self.request.user, context['member_groups'])
        context['sent_requests'] = getMyPendingRequests(self.request.user)
        # print(context['member_groups'])
        return context


class MyGroups(TemplateView):
    template_name = 'admin_groups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_groups'] = getOwnedGroups(self.request.user)
        my_groups = getOwnedGroups(self.request.user)
        incoming_requests = []
        for group in my_groups:
            incoming_requests += (getPendingRequests(group))
        # print(context['my_groups'])
        context['incoming_requests'] = incoming_requests
        print(context)
        return context


def groupsView(request, group_id):
    if not request.user.is_authenticated:
        raise PermissionDenied
    # group_id = request.POST.get("group_id", "default")
    group = Groups.objects.get(id=group_id)
    obj = Groups.objects.get(pk=group_id)
    x = giveGroupMembers(obj)
    all_posts = getGroupPosts(group)
    # pending_requests = getPendingRequests(obj)
    # context = {'members': x, 'group_id': group_id, 'member_requests': pending_requests}
    context = {'members': x, 'group_id': group_id, 'group' : group, 'all_posts' : all_posts}
    return render(request, 'group_view.html', context)


def AddJoinRequest(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    group_id = request.POST.get("group_id", "default")
    new_member = Group_Members.objects.create(member=request.user, group_id=group_id, confirmed=False)
    new_member.save()
    return HttpResponseRedirect(reverse('groups:group'))


def addgroup(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    num_groups = len(getOwnedGroups(request.user))
    allowed_groups = float("inf")
    if request.user.user_type == 2:
        allowed_groups = 2
    elif request.user.user_type == 3:
        allowed_groups = 4

    if num_groups >= allowed_groups:
        return utils.raise_exception(request, "You have reached the limit of adding groups (" + str(allowed_groups) + ")")
    if request.method == "POST":
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            description = form.cleaned_data['description']
            fees = form.cleaned_data['fees']
            obj = Groups.objects.create(group_name=group_name, description=description, fees=fees, admin_id=request.user.id)
            obj.save()
            return HttpResponseRedirect(reverse('groups:add_group'))
    else:
        form = GroupCreateForm()
    return render(request, 'create_group.html', {'form': form})


def cancelJoinRequest(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    group_id = request.POST.get("group_id", "default")
    # print(group_id, request.user)
    Group_Members.objects.filter(member=request.user, group_id=group_id).delete()
    return HttpResponseRedirect(reverse('groups:group'))


def removeFromGroup(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    group_id = request.POST.get("group_id", "default")
    Group_Members.objects.filter(member=request.user, group_id=group_id).delete()
    return HttpResponseRedirect(reverse('groups:group'))


def acceptJoinRequest(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    group_id = request.POST.get("group_id", "default")
    member_id = request.POST.get("member_id", "default")
    # print(group_id, member_id)
    obj = Group_Members.objects.get(member_id=member_id, group_id=group_id)
    obj.confirmed = True
    obj.save()
    return HttpResponseRedirect(reverse('groups:group_admin'))


def rejectJoinRequest(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    group_id = request.POST.get("group_id", "default")
    member_id = request.POST.get("member_id", "default")
    Group_Members.objects.get(member_id=member_id, group_id=group_id).delete()
    return HttpResponseRedirect(reverse('groups:group_admin'))

def add_group_post(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    group_id = request.POST.get("group_id", "null")
    member_id = request.POST.get("member_id", "null")
    post_text = request.POST.get("post_text", "null")

    group = Groups.objects.get(id=group_id)
    member = CustomUser.objects.get(id=member_id)
    Group_Posts.objects.create(group=group, author=member, description=post_text)
    return HttpResponseRedirect(reverse('groups:group_view', kwargs={'group_id':group_id}))