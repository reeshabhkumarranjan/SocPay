from friends.models import Friend
from private_message.models import Private_Message
from users.models import CustomUser
from groups.models import Groups, Group_Posts, Group_Members
from commercial_page.models import CommercialPage
from django.db.models import Q

def populate():
    print("Clearing database...")
    CustomUser.objects.filter(~Q(username='admin')).delete()
    Friend.objects.all().delete()

    print("Creating Users...")
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

    print("Creating Friendships...")
    senders = [fahad, reeshabh, krishna, rohan]
    receivers = [fahad, reeshabh, krishna, rohan]

    for i in range(4):
        for j in range(i + 1 , 4):
            if i==j:
                continue
            confirmed = True
            if receivers[j] == rohan:
                confirmed = False
            friend = Friend.objects.create(creator=senders[i], follower=receivers[j], confirmed=confirmed)
            friend.save()

    print("Creating Groups...")
    group1 = Groups.objects.create(admin=reeshabh, group_name="Reeshabh's Group", fees=0, description="This is Reeshabh's Group")
    member1 = Group_Members.objects.create(group=group1, member=fahad, confirmed=True)
    member2 = Group_Members.objects.create(group=group1, member=krishna, confirmed=False)

    print("Creating Messages...")
    private_message1 = Private_Message(sender=reeshabh, receiver=fahad, message="Hi How are you??")
    private_message1.save()
    private_message2 = Private_Message(sender=fahad, receiver=reeshabh, message="Hi I am fine")
    private_message2.save()
    private_message3 = Private_Message(sender=reeshabh, receiver=fahad, message="Kem cho??")
    private_message3.save()
    private_message4 = Private_Message(sender=fahad, receiver=reeshabh, message="Majama")
    private_message4.save()

    print("Creating Pages...")
    page1 = CommercialPage(page_name="Reeshabh's Page", admin=reeshabh, description="This is Reeshabh's page!")
    page1.save()

    print("Done!")