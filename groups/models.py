from django.db import models
from users.models import CustomUser

class Groups(models.Model):
    group_name = models.CharField(default="", max_length=200)
    admin = models.ForeignKey(CustomUser, related_name="admin", on_delete=models.CASCADE)
    fees = models.IntegerField(default=0)
    description = models.CharField(default="", max_length=200)
    member_deletion_access = models.IntegerField(default=0)
    post_view_access = models.IntegerField(default=0)

    def __str__(self):
        return str(self.group_name) + " " + str(self.admin) + " " + str(self.fees) + " " + str(self.description)


class Group_Members(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.group) + " " + str(self.member) + " " + str(self.confirmed)


class Group_Posts(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(default="", max_length=1000)
    date = models.DateTimeField(auto_now_add=True)


def giveMyGroups(user):
    my_groups = Group_Members.objects.filter(member=user, confirmed=True).values_list("group")
    arr = []
    for i in my_groups:
        arr.append(Groups.objects.get(id=i[0]))
    return arr


def giveGroupMembers(group):
    members = Group_Members.objects.filter(group=group, confirmed=True).values_list("member")
    arr = []
    for i in members:
        arr.append(CustomUser.objects.get(id=i[0]))
    return arr


def isAdmin(user, group):
    obj = Groups.objects.filter(admin=user, id=group.id)
    return len(obj) != 0


def getAdmin(group):
    return group.admin


def getPendingRequests(group):
    members = Group_Members.objects.filter(group=group, confirmed=False)
    # arr = []
    # for i in members:
    #     arr.append(CustomUser.objects.get(id=i[0]))
    return members


def getFees(group):
    return group.fees


def getOwnedGroups(user):
    group = Groups.objects.filter(admin=user)
    return group


def getGroupPosts(group):
    posts = Group_Posts.objects.filter(group=group)
    return posts


def getMyPendingRequests(user):
    my_groups = Group_Members.objects.filter(member=user, confirmed=False).values_list("group")
    arr = []
    for i in my_groups:
        arr.append(Groups.objects.get(id=i[0]))
    return arr


def giveOtherGroups(user, my_groups):
    other_groups = Groups.objects.all()
    admin_groups = getOwnedGroups(user)
    requested_groups = getMyPendingRequests(user)
    arr = []
    for i in other_groups:
        if i not in my_groups and i not in admin_groups and i not in requested_groups:
            arr.append(i)
    return arr
