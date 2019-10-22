from django.contrib import admin

# Register your models here.
from .models import Transaction, Post

admin.site.register(Transaction)
admin.site.register(Post)