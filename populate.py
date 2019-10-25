from users.models import CustomUser, Friend
from django.db.models import Q
from groups.models import Groups, Group_Members, Group_Posts
from private_message.models import Private_Message

def populate():
    print("Creating users")
    CustomUser.objects.filter(~Q(username='admin')).delete()
    Friend.objects.all().delete()
    user = []
    for i in range(10):
        useri = CustomUser.objects.create(username="user{0}".format(i + 1))
        useri.set_password("user{0}".format(i + 1))
        useri.save()
        user.append(useri)

    for i in range(10):
        for j in range(3):
            k = (i + j) % 10
            if k % 2 == 0:
                friend = Friend.objects.create(creator=user[i], follower=user[k], confirmed=True)
                friend.save()
            else:
                friend = Friend.objects.create(creator=user[i], follower=user[k], confirmed=False)
                friend.save()

    groups = []
    for i in range(3):
        group = Groups.objects.create(admin=user[i], group_name="group{0}".format(i + 1), fees=0,
                                      description="description{0}".format(i + 1))
        group.save()
        groups.append(group)
        k1 = (i + 1) % 10
        k2 = (i + 2) % 10
        member = Group_Members.objects.create(group=group, member=user[k1], confirmed=True)
        member.save()
        member = Group_Members.objects.create(group=group, member=user[k2], confirmed=False)
        member.save()

    private_message1 = Private_Message(sender=user[0], receiver=user[1], message="Hi How are you??")
    private_message1.save()
    private_message2 = Private_Message(sender=user[1], receiver=user[0], message="Hi I am fine")
    private_message2.save()
    private_message3 = Private_Message(sender=user[0], receiver=user[1], message="Kem cho??")
    private_message3.save()
