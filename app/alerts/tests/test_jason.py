from django.test import TestCase
from users.models import User
from teams.models import Team, Invite
from alerts.models import Alert, Target


class AlertsTestCases(TestCase):
    # jason
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

    # jason
    def test_alert_read_toggle_false(self):
        u = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        u.save()
        a = Alert(user=u, read=True)
        a.save()
        a.read=False
        self.assertEqual(a.read, False)

    # jason
    def test_alert_body_change_to_null(self):
        u = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        u.save()
        a = Alert(user=u, body='this is a test message')
        a.save()
        a.body=''
        self.assertEqual(a.body, '')
