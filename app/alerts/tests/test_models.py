from django.test import TestCase
from alerts.models import Alert, Target
from contests.models import Contest
from teams.models import Team, Invite, JoinRequest
from users.models import User

class TargetTest(TestCase):

    fixtures = ['users.json', 'teams.json', 'contests.json']

    # nathan
    def test_href_user(self):
        target = Target(user=User.objects.get(pk=1))
        self.assertNotEqual('', target.href())

    # nathan
    def test_href_team(self):
        target = Target(team=Team.objects.get(pk=1))
        self.assertNotEqual('', target.href())

    # nathan
    def test_href_invite(self):
        user = User.objects.get(pk=1)
        team = Team.objects.get(pk=1)
        invite = Invite(user=user, team=team)
        target = Target(invite=invite)
        self.assertNotEqual('', target.href())

    # nathan
    def test_href_join_request(self):
        user = User.objects.get(pk=1)
        team = Team.objects.get(pk=1)
        join_request = JoinRequest(user=user, team=team)
        target = Target(join_request=join_request)
        self.assertNotEqual('', target.href())

    # nathan
    def test_href_contest(self):
        target = Target(contest=Contest.objects.get(pk=1))
        self.assertNotEqual('', target.href())

    # nathan
    def test_href_url(self):
        target = Target(url='http://www.google.com/')
        self.assertEqual(target.href(), 'http://www.google.com/')

    # nathan
    def test_href_none(self):
        target = Target()
        self.assertEqual('', target.href())
        

class AlertTest(TestCase):

    fixtures = ['users.json']

    # nathan
    def test_href_target(self):
        target = Target(url='http://www.google.com/')
        alert = Alert(user=User.objects.get(pk=1), target=target)
        self.assertEqual(alert.href(), target.href())

    # nathan
    def test_href_without_target(self):
        alert = Alert(user=User.objects.get(pk=1))
        self.assertEqual(alert.href(), '')
