from users.models import CustomUser, Friend
from django.db.models import Q
from groups.models import Groups, Group_Members, Group_Posts

def populate():
    print("Clearing database")
    CustomUser.objects.filter(~Q(username='admin')).delete()
    Friend.objects.all().delete()

    print("Creating Users")
    fahad = CustomUser.objects.create(username="fahad", first_name="Fahad")
    reeshabh = CustomUser.objects.create(username="reeshabh", first_name="Reeshabh")
    krishna = CustomUser.objects.create(username="krishna", first_name="Krishna")
    rohan = CustomUser.objects.create(username="rohan", first_name="Rohan")
    anon = CustomUser.objects.create(username="anonymous", first_name="Anonymous")

    fahad.set_password("p4nr44cfv4")
    reeshabh.set_password("2e8bzp7pzx")
    krishna.set_password("v8qrz4g73q")
    rohan.set_password("gtajqz25mj")
    anon.set_password("tgnsy53std")

    fahad.save()
    reeshabh.save()
    krishna.save()
    rohan.save()
    anon.save()

    print("Creating Friendships")
    senders = [fahad, reeshabh, krishna, rohan]
    receivers = [fahad, reeshabh, krishna, rohan]

    for i in range(4):
        for j in range(i + 1, 4):
            if i == j:
                continue
            confirmed = True
            if receivers[j] == rohan:
                confirmed = False
            friend = Friend.objects.create(creator=senders[i], follower=receivers[j], confirmed=confirmed)
            friend.save()
