from django.db import models
from users.models import CustomUser


class Private_Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="message_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="message_receiver", on_delete=models.CASCADE)
    message = models.CharField(default="", max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "sender: " + str(self.sender.username) + " receiver: " + str(self.receiver.username) + " message: " + str(self.message) + " datetime: " + str(self.datetime)
    # date = models.DateField(auto_now_add=True)
    # time = models.TimeField(auto_now_add=True)


def getAllMessages(user1, user2):
    messages = list(Private_Message.objects.filter(sender=user1, receiver=user2) | Private_Message.objects.filter(sender=user2, receiver=user1))
    messages = sorted(messages, key=lambda x:x.datetime)
    # messages.order_by('datetime')
    #messages.sort(key=lambda x: (x.date, x.time))
    return messages