from django.contrib import admin
from models import UserGroup, UserProfile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass


class GroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserAdmin)
admin.site.register(UserGroup, GroupAdmin)