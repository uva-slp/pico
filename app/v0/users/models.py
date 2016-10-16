from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import datetime


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    administrator = models.BooleanField(default=0)
    suspended = models.BooleanField(default=1)

    @property
    def is_admin(self):
        return bool(self.administrator)

    def make_admin(self, admin):
        self.administrator = admin

    @property
    def date_joined(self):
        return self.user.date_joined

    @property
    def is_suspended(self):
        return bool(self.suspended)


class UserGroup(models.Model):
    group = models.OneToOneField(Group)

    @property
    def user_set(self):
        return self.group.user_set

    def __str__(self):
        return self.group.name