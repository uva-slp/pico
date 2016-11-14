from django.urls import reverse
from django.test import TestCase

from users.backends import ModelBackend

class GetUserTest(TestCase):

	fixtures = ['users.json']

	def setUp(self):
		self.backend = ModelBackend()

	def test_valid_user_id(self):
		user = self.backend.get_user(1)

		self.assertIsNotNone(user)

	def test_invalid_user_id(self):
		user = self.backend.get_user(-1)

		self.assertIsNone(user)
