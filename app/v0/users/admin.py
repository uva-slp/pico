from django.contrib import admin

from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User as AuthUser, Group

from .models import User, Team


admin.site.unregister(AuthUser)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Team, GroupAdmin)
