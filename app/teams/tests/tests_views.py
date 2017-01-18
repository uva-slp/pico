from django.urls import reverse
from django.test import TestCase

from teams.models import Team
from users.models import User

class CreateTeamTest(TestCase):

	fixtures = ['users.json']

	# nathan
	def test_post(self):
		self.client.login(username='testuser', password='password')
		data = {
			'name': 'Team 1',
		}
		resp = self.client.post(reverse('teams:create'), data=data)

		self.assertTrue(Team.objects.filter(name='Team 1').exists())
		self.assertEqual(resp.status_code, 200)

class JoinTeamTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	# nathan
	def test_post(self):
		self.client.login(username='testuser', password='password')
		data = {
			'team': '1',
		}
		resp = self.client.post(reverse('teams:join'), data=data)

		team = Team.objects.get(pk=1)
		self.assertTrue(team.members.filter(username='testuser').exists())

class LeaveTeamTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	# nathan
	def test_post(self):
		Team.objects.get(pk=1).members.add(User.objects.get(pk=1))
		self.client.login(username='testuser', password='password')
		data = {
			'team': '1',
		}
		resp = self.client.post(reverse('teams:leave'), data=data)

		team = Team.objects.get(pk=1)
		self.assertFalse(team.members.filter(username='testuser').exists())

class AutocompleteTest(TestCase):

	fixtures = ['teams.json']

	# nathan
	def test_post(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('teams:autocomplete'))
		
		self.assertEqual(resp.status_code, 200)
