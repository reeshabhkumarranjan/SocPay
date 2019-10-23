from django.contrib import admin

# Register your models here.
from users.models import Friend, CustomUser
from .models import Transaction, Post

admin.site.register(Transaction)
admin.site.register(Post)
admin.site.register(Friend)
admin.site.register(CustomUser)