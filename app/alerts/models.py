from django.db import models
from django.urls import reverse

from users.models import User
from teams.models import Team
from contests.models import Contest

MAX_LENGTH = 160

class Alert(models.Model):
    user = models.ForeignKey(User, related_name='alerts')
    subject = models.CharField(max_length=25, blank=True)
    body = models.CharField(max_length=MAX_LENGTH, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def href(self):
        target = Target.objects.get(alert=self)
        if target:
            return target.href()
        return ''

class Target(models.Model):
    alert = models.OneToOneField(Alert, related_name='target')
    user = models.ForeignKey(User, null=True, blank=True)
    team = models.ForeignKey(Team, null=True, blank=True)
    contest = models.ForeignKey(Contest, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)

    def href(self):
        if self.user:
            return ''
        if self.team:
            return ''
        if self.contest:
            return ''
        if self.url:
            return url
        return ''

