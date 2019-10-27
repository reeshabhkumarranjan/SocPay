from django.contrib import admin
from .models import Groups, Group_Members, Group_Posts

admin.site.register(Groups)
admin.site.register(Group_Members)
admin.site.register(Group_Posts)
