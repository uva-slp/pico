from django.db import models
from django.urls import reverse

from users.models import User
from teams.models import Team, Invite, JoinRequest
from contests.models import Contest

MAX_LENGTH = 160

class Target(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    invite = models.ForeignKey(Invite, null= True, blank=True, on_delete=models.CASCADE)
    join_request = models.ForeignKey(JoinRequest, null=True, blank=True, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, null=True, blank=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=200, null=True, blank=True)

    def href(self):
        if self.user:
            return reverse('users:view', kwargs={'user_id': self.user.id})
        if self.team:
            return reverse('teams:index', kwargs={'team_id': self.team.id})
        if self.invite:
            return reverse('teams:index', kwargs={'team_id': self.invite.team.id})
        if self.join_request:
            return reverse('teams:index', kwargs={'team_id': self.join_request.team.id})
        if self.contest:
            return reverse('contests:contest', kwargs={'contest_id': self.contest.id})
        if self.url:
            return self.url
        return ''

class Alert(models.Model):
    user = models.ForeignKey(User, related_name='alerts')
    subject = models.CharField(max_length=25, blank=True)
    body = models.CharField(max_length=MAX_LENGTH, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    target = models.ForeignKey(Target, related_name='alert', null=True, blank=True, on_delete=models.CASCADE)

    def href(self):
        if self.target:
            return self.target.href()
        return ''

