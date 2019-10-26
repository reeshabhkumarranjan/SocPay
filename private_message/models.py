from django.db import models
from users.models import CustomUser


class Private_Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="message_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="message_receiver", on_delete=models.CASCADE)
    message = models.CharField(default="", max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)


def getAllMessages(user1, user2):
    messages = Private_Message.objects.filter(sender=user1, receiver=user2) | Private_Message.objects.filter(sender=user2, receiver=user1)
    #messages.sort(key=lambda x: (x.date, x.time))
    return messages
