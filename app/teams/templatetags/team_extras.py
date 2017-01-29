from django import template

from teams.models import Invite

register = template.Library()

@register.filter
def has_invite(user, team):
    return Invite.objects.filter(user=user, team=team).exists()
