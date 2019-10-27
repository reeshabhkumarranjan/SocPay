from django.contrib import admin

# Register your models here.
from wallet.models import Transaction

admin.site.register(Transaction)