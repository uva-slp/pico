from django.test import TestCase
from users.models import User
from teams.models import Team, Invite
from alerts.models import Alert, Target

class AlertsTestCases(TestCase):
    #jason
    def testAlertCount(self):
        u = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        u.save()
        a = Alert(user=u)
        b = Alert(user=u)
        c = Alert(user=u)
        a.save()
        b.save()
        c.save()
        alerts_count = Alert.objects.all().count()
        self.assertEqual(alerts_count, 3)

    #jason
    def test_alert_read_toggle_false(self):
        u = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        u.save()
        a = Alert(user=u, read=True)
        a.save()
        a.read=False
        self.assertEqual(a.read, False)

    #jason
    def test_alert_body_change_to_null(self):
        u = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        u.save()
        a = Alert(user=u, body='this is a test message')
        a.save()
        a.body=''
        self.assertEqual(a.body, '')

    #jason
    def test_target_team_switch(self):
        u = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        t1 = Team(name='team1')
        t2 = Team(name='team2')
        u.save()
        a = Alert(user=u)
        t1.save()
        t2.save()
        a.save()
        tar = Target(alert=a, user=u, team=t1)
        tar.save()
        tar.team=t2
        self.assertEqual(tar.team, t2)

    #jason
    def test_target_user_switch(self):
        u1 = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        u2 = User(username='buddy2', password='jgd3hb222', email='buddy2@gmail.com')
        t = Team(name='team')
        u1.save()
        u2.save()
        a = Alert(user=u1)
        t.save()
        a.save()
        tar = Target(alert=a, user=u1, team=t)
        tar.save()
        tar.user=u2
        self.assertEqual(tar.user, u2)
