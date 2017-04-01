from django.contrib import auth
from django.urls import reverse
from django.test import TestCase

from teams.models import Team, JoinRequest, Invite
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

class CreateTest(TestCase):

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

class JoinTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)

	# nathan
	def test_get(self):
		resp = self.client.get(reverse('teams:join'))
		self.assertRedirects(resp, reverse('teams:index'), 302, 200)

	# nathan
	def test_post(self):
		team = Team.objects.get(pk=1)
		data = {
			'team': team.id,
		}
		resp = self.client.post(reverse('teams:join'), data=data)
		self.assertTrue(self.user in team.members.all())

	# nathan
	def test_already_member(self):
		team = Team.objects.get(pk=1)
		team.members.add(self.user)
		team.save()
		data = {
			'team': team.id,
		}
		resp = self.client.post(reverse('teams:join'), data=data)
		self.assertRedirects(resp, reverse('teams:index', kwargs={'team_id':team.id}), 302, 200)

	# nathan
	def test_private(self):
		team = Team.objects.filter(public=False).first()
		data = {
			'team': team.id,
		}
		resp = self.client.post(reverse('teams:join'), data=data)
		self.assertTrue(JoinRequest.objects.filter(team=team, user=self.user).exists())
		self.assertFalse(self.user in team.members.all())

class InviteTest(TestCase):

	fixtures = ['users.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')

	# nathan
	def test_get(self):
		resp = self.client.get(reverse('teams:invite', kwargs={'action':'send'}))
		self.assertRedirects(resp, reverse('teams:index'), 302, 200)

class SendInviteTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)
		self.user_other = User.objects.exclude(id=self.user.id).first()
		self.team = Team.objects.filter(public=False).first()
		self.team.members.add(self.user)
		self.team.members.remove(self.user_other)
		self.team.save()

	# nathan
	def test(self):
		data = {
			'team': self.team.id,
			'user': self.user_other.id
		}
		resp = self.client.post(reverse('teams:invite', kwargs={'action':'send'}), data=data)
		self.assertRedirects(resp,reverse('teams:index', kwargs={'team_id':self.team.id}), 302, 200)
		self.assertTrue(Invite.objects.filter(team=self.team, user=self.user_other).exists())

	# nathan
	def test_unauthorized(self):
		team = Team.objects.exclude(id=self.team.id).first()
		team.members.remove(self.user)
		team.members.remove(self.user_other)
		team.save()

		data = {
			'team': team.id,
			'user': self.user_other.id
		}
		resp = self.client.post(reverse('teams:invite', kwargs={'action':'send'}), data=data)
		
		self.assertRedirects(resp,reverse('teams:index', kwargs={'team_id':team.id}), 302, 200)
		self.assertFalse(Invite.objects.filter(team=team, user=self.user_other).exists())

	# nathan
	def test_already_member(self):
		self.team.members.add(self.user_other)
		self.team.save()

		data = {
			'team': self.team.id,
			'user': self.user_other.id
		}
		resp = self.client.post(reverse('teams:invite', kwargs={'action':'send'}), data=data)
		self.assertRedirects(resp,reverse('teams:index', kwargs={'team_id':self.team.id}), 302, 200)
		self.assertFalse(Invite.objects.filter(team=self.team, user=self.user_other).exists())

		self.team.members.remove(self.user_other)
		self.team.save()

	# nathan
	def test_invite_exists(self):
		invite = Invite(user=self.user_other, team=self.team)
		invite.save()

		data = {
			'team': self.team.id,
			'user': self.user_other.id
		}
		resp = self.client.post(reverse('teams:invite', kwargs={'action':'send'}), data=data)
		self.assertRedirects(resp,reverse('teams:index', kwargs={'team_id':self.team.id}), 302, 200)
		self.assertTrue(Invite.objects.filter(team=self.team, user=self.user_other).exists())

		invite.delete()

class AcceptInviteTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)
		self.team = Team.objects.filter(public=False).first()
		self.team.members.remove(self.user)
		self.team.save()
		self.invite = Invite(user=self.user, team=self.team)
		self.invite.save()

	# nathan
	def test(self):
		data = {
			'team': self.team.id
		}
		resp = self.client.post(reverse('teams:invite', kwargs={'action':'accept'}), data=data)
		self.assertRedirects(resp,reverse('teams:index', kwargs={'team_id':self.team.id}), 302, 200)
		self.assertFalse(Invite.objects.filter(team=self.team, user=self.user).exists())
		self.assertTrue(self.user in self.team.members.all())

class DeclineInviteTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)
		self.team = Team.objects.filter(public=False).first()
		self.team.members.remove(self.user)
		self.team.save()
		self.invite = Invite(user=self.user, team=self.team)
		self.invite.save()

	# nathan
	def test(self):
		data = {
			'team': self.team.id
		}
		resp = self.client.post(reverse('teams:invite', kwargs={'action':'decline'}), data=data)
		self.assertRedirects(resp,reverse('teams:index', kwargs={'team_id':self.team.id}), 302, 200)
		self.assertFalse(Invite.objects.filter(team=self.team, user=self.user).exists())
		self.assertFalse(self.user in self.team.members.all())

class CancelInviteTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)
		self.user_other = User.objects.exclude(id=self.user.id).first()
		self.team = Team.objects.filter(public=False).first()
		self.team.members.add(self.user)
		self.team.members.remove(self.user_other)
		self.team.save()
		self.invite = Invite(user=self.user_other, team=self.team)
		self.invite.save()

	# nathan
	def test(self):
		data = {
			'invite': self.invite.id
		}
		resp = self.client.post(reverse('teams:invite', kwargs={'action':'cancel'}), data=data)
		self.assertRedirects(resp,reverse('teams:index', kwargs={'team_id':self.team.id}), 302, 200)
		self.assertFalse(Invite.objects.filter(team=self.team, user=self.user_other).exists())
		self.assertFalse(self.user_other in self.team.members.all())

class JoinRequestTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)
		self.user_other = User.objects.exclude(id=self.user.id).first()
		self.user_other.set_password('password')
		self.user_other.save()
		self.team = Team.objects.filter(public=False).first()
		self.team.members.add(self.user)
		self.team.members.remove(self.user_other)
		self.team.save()
		self.join_request = JoinRequest(user=self.user_other, team=self.team)
		self.join_request.save()

	# nathan
	def test_get(self):
		resp = self.client.get(reverse('teams:join-request', kwargs={'action':'accept'}))
		self.assertRedirects(resp, reverse('teams:index'), 302, 200)

	# nathan
	def test_accept(self):
		data = {
			'join_request': self.join_request.id
		}
		resp = self.client.post(reverse('teams:join-request', kwargs={'action':'accept'}), data=data)
		self.assertRedirects(resp, reverse('teams:index', kwargs={'team_id':self.join_request.team.id}), 302, 200)
		self.assertFalse(JoinRequest.objects.filter(id=self.join_request.id).exists())
		self.assertTrue(self.user_other in self.team.members.all())

	# nathan
	def test_decline(self):
		data = {
			'join_request': self.join_request.id
		}
		resp = self.client.post(reverse('teams:join-request', kwargs={'action':'decline'}), data=data)
		self.assertRedirects(resp, reverse('teams:index', kwargs={'team_id':self.join_request.team.id}), 302, 200)
		self.assertFalse(JoinRequest.objects.filter(id=self.join_request.id).exists())
		self.assertFalse(self.user_other in self.team.members.all())

	# nathan
	def test_cancel(self):
		self.client.logout()
		self.client.login(username=self.user_other.username, password='password')
		data = {
			'join_request': self.join_request.id
		}
		resp = self.client.post(reverse('teams:join-request', kwargs={'action':'cancel'}), data=data)
		self.assertRedirects(resp, reverse('teams:index', kwargs={'team_id':self.join_request.team.id}), 302, 200)
		self.assertFalse(JoinRequest.objects.filter(id=self.join_request.id).exists())

class IsPublicTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)
		self.team = Team.objects.first()
		self.team.members.add(self.user)
		self.team.save()

	# nathan
	def test_get(self):
		resp = self.client.get(reverse('teams:public'))
		self.assertRedirects(resp, reverse('teams:index'), 302, 200)

	# nathan
	def test_public(self):
		data = {
			'team': self.team.id,
			'public': 'on'
		}
		resp = self.client.post(reverse('teams:public'), data=data)
		json = resp.json()
		self.assertEqual(resp.status_code, 200)
		self.assertDictEqual(json, {'public': True})

	# nathan
	def test_private(self):
		data = {
			'team': self.team.id,
			'public': 'off'
		}
		resp = self.client.post(reverse('teams:public'), data=data)
		json = resp.json()
		self.assertEqual(resp.status_code, 200)
		self.assertDictEqual(json, {'public': False})

class GetTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)
		self.team = Team.objects.first()
		self.team.members.add(self.user)
		self.team.save()

	# nathan
	def test_get(self):
		resp = self.client.get(reverse('teams:get'))
		self.assertRedirects(resp, reverse('teams:index'), 302, 200)

	# nathan
	def test_post(self):
		data = {
			'team': self.team.id,
		}
		resp = self.client.post(reverse('teams:get'), data=data)
		json = resp.json()
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('tab' in json and 'panel' in json)

	# nathan
	def test_post_error(self):
		resp = self.client.post(reverse('teams:get'), data={})
		json = resp.json()
		self.assertEqual(resp.status_code, 201)
		self.assertDictEqual(json, {})

class LeaveTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)
		self.team = Team(name='team-with-one-user')
		self.team.save()
		self.team.members.add(self.user)
		self.team.save()

	# nathan
	def test_get(self):
		resp = self.client.get(reverse('teams:leave'))
		self.assertRedirects(resp, reverse('teams:index'), 302, 200)

	# nathan
	def test_post(self):
		data = {
			'team': self.team.id
		}
		resp = self.client.post(reverse('teams:leave'), data=data)
		json = resp.json()
		self.assertEqual(resp.status_code, 200)
		self.assertDictEqual(json, {})

class AutocompleteTest(TestCase):

	fixtures = ['users.json', 'teams.json']

	# nathan
	def test_post(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('teams:autocomplete'))
		
		self.assertEqual(resp.status_code, 200)

	# nathan
	def test_unauthenticated(self):
		resp = self.client.get(reverse('teams:autocomplete'))
		self.assertQuerysetEqual(resp.json()['results'], Team.objects.none())

	# nathan
	def test_authenticated(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('teams:autocomplete'))
		list1 = [item['text'] for item in resp.json()['results']]
		list2 = [team.name for team in Team.objects.all().order_by('id')[:10]]
		self.assertListEqual(list1, list2)

	# nathan
	def test_authenticated_query(self):
		self.client.login(username='testuser', password='password')
		q = 'team'
		resp = self.client.get(reverse('teams:autocomplete'), data={'q':q})
		list1 = [item['text'] for item in resp.json()['results']]
		list2 = [team.name for team in Team.objects.filter(name__istartswith=q).order_by('id')[:10]]
		self.assertListEqual(list1, list2)
