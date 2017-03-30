from django.test import TestCase

from users.lib import storage
from users.models import User

class UserTest(TestCase):

    fixtures = ['profiles.json']

    # nathan
    def test_get_profile_exists(self):
        user = User.objects.get(pk=1)
        self.assertIsNotNone(user.get_profile())
    
    # nathan
    def test_get_profile_nonexistant(self):
        user = User()
        self.assertIsNotNone(user.get_profile())
