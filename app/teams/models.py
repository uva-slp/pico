from django.db import models

from users.models import User

class Team(models.Model):
    name = models.CharField(max_length=32, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='teams')
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Invite(models.Model):
    team = models.ForeignKey(Team, related_name='invites')
    user = models.ForeignKey(User, related_name='team_invites')
    timestamp = models.DateTimeField(auto_now_add=True)

class JoinRequest(models.Model):
    team = models.ForeignKey(Team, related_name='join_requests')
    user = models.ForeignKey(User, related_name='team_join_requests')
    timestamp = models.DateTimeField(auto_now_add=True)
