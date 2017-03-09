from django.urls import reverse
from django.test import TestCase

from teams.models import Team
from users.models import User

class IndexTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	# nathan
	def test_default(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('teams:index'))
		self.assertEqual(resp.status_code, 200)
	
	# nathan
	def test_team_id(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('teams:index', kwargs={'team_id':1}))
		self.assertEqual(resp.status_code, 200)
	
	# nathan
	def test_invalid_team_id(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('teams:index', kwargs={'team_id':9999}))
		self.assertRedirects(resp, reverse('teams:index'))

class CreateTeamTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	# nathan
	def test_post(self):
		self.client.login(username='testuser', password='password')
		data = {
			'name': 'UNUSED_TEAM_NAME',
		}
		resp = self.client.post(reverse('teams:create'), data=data)

		self.assertTrue(Team.objects.filter(name='Team 1').exists())
		self.assertEqual(resp.status_code, 200)

	# nathan
	def test_form_error(self):
		self.client.login(username='testuser', password='password')
		data = {
			'name': Team.objects.first().name # duplicate name
		}
		resp = self.client.post(reverse('teams:create'), data=data)

		self.assertEqual(resp.status_code, 201)

	# nathan
	def test_get(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('teams:create'))

		self.assertRedirects(resp, reverse('teams:index'))

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

	fixtures = ['users.json', 'teams.json']

	# nathan
	def test_post(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('teams:autocomplete'))
		
		self.assertEqual(resp.status_code, 200)
