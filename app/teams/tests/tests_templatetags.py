from django.test import TestCase

from teams.templatetags import team_extras
from teams.models import Team, Invite, JoinRequest
from users.models import User

class TeamExtrasTest(TestCase):

    fixtures = ['users.json', 'teams.json']
    
    # nathan
    def test_has_invite(self):
        team = Team.objects.get(id=1)
        user = User.objects.get(id=1)
        
        self.assertFalse(team_extras.has_invite(user, team))
    
    # nathan
    def test_has_request(self):
        team = Team.objects.get(id=1)
        user = User.objects.get(id=1)
        
        self.assertFalse(team_extras.has_request(team, user))
    
    # nathan
    def test_get_request(self):
        team = Team.objects.get(id=1)
        user = User.objects.get(id=1)
        
        self.assertIsNone(team_extras.get_request(team, user))
