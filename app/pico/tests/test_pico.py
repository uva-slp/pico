from django.test import TestCase
from users.models import User
from teams.models import Team, Invite
from alerts.models import Alert, Target


class PicoTest(TestCase):
    # nathan
    def test_wsgi(self):
        from pico import wsgi
