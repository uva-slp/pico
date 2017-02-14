from django.test import TestCase
from users.models import User
from alerts.models import Alert

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