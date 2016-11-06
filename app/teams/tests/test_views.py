from django.urls import reverse
from django.test import TestCase

class CreateTeamTest(TestCase):

	fixtures = ['users.json']

	def test_post(self):
		self.client.login(username='testuser', password='password')
		data = {
			'name': 'Team 1',
		}
		resp = self.client.post(reverse('teams:create'), data=data)

		self.assertRedirects(resp, reverse('contests:home'), status_code=302, target_status_code=200)

class JoinTeamTest(TestCase):

	fixtures = ['users.json']

	def test_post(self):
		self.client.login(username='testuser', password='password')
		
