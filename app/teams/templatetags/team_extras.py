from django import template

from teams.models import Invite, JoinRequest

register = template.Library()

@register.filter
def has_invite(user, team):
    return Invite.objects.filter(user=user, team=team).exists()

@register.filter
def get_invite(user, team):
    return Invite.objects.filter(user=user, team=team).first()

@register.filter
def has_request(team, user):
    return JoinRequest.objects.filter(user=user, team=team).exists()

@register.filter
def get_request(team, user):
    return JoinRequest.objects.filter(user=user, team=team).first()
