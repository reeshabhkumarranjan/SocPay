from django.contrib.auth.models import Group

from friends.models import Friend
from main_app.models import Post
from private_message.models import Private_Message
from users.models import CustomUser
from groups.models import Groups, Group_Posts, Group_Members
from commercial_page.models import CommercialPage, CommercialPagePosts
from django.db.models import Q

from wallet.models import Transaction


def populate():
    print("Clearing database...")
    Group.objects.all().delete()
    CommercialPagePosts.objects.all().delete()
    CommercialPage.objects.all().delete()
    Friend.objects.all().delete()
    Group_Members.objects.all().delete()
    Groups.objects.all().delete()
    Group_Posts.objects.all().delete()
    Post.objects.all().delete()
    Private_Message.objects.all().delete()
    CustomUser.objects.filter(~Q(username='admin')).delete()
    Transaction.objects.all().delete()

    print("Creating Users...")
    fahad = CustomUser.objects.create(username="fahad", first_name="Fahad", email="fahad17049@iiitd.ac.in")
    reeshabh = CustomUser.objects.create(username="reeshabh", first_name="Reeshabh", email="reeshabh17086@iiitd.ac.in")
    krishna = CustomUser.objects.create(username="krishna", first_name="Krishna", email="krishna17060@iiitd.ac.in")
    rohan = CustomUser.objects.create(username="rohan", first_name="Rohan", email="rohan17088@iiitd.ac.in")
    anon = CustomUser.objects.create(username="anonymous", first_name="Anonymous")

    fahad.set_password("p4nr44cfv4")
    reeshabh.set_password("e4hwgs3xj9")
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