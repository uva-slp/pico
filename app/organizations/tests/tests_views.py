from django.urls import reverse
from django.test import TestCase

from organizations.models import Organization
from users.models import User

class CreateOrganizationTest(TestCase):

	fixtures = ['users.json']

	# nathan
	def test_post(self):
		self.client.login(username='testuser', password='password')
		data = {
			'name': 'Organization 1',
		}
		resp = self.client.post(reverse('organizations:create'), data=data)

		self.assertRedirects(resp, reverse('home'), status_code=302, target_status_code=200)

class JoinOrganizationTest(TestCase):

	fixtures = ['users.json', 'organizations.json']

	# nathan
	def test_post(self):
		self.client.login(username='testuser', password='password')
		data = {
			'organization': '1',
		}
		resp = self.client.post(reverse('organizations:join'), data=data)

		org = Organization.objects.get(pk=1)
		self.assertTrue(org.members.filter(username='testuser').exists())

class LeaveOrganizationTest(TestCase):

	fixtures = ['users.json', 'organizations.json']

	# nathan
	def test_post(self):
		Organization.objects.get(pk=1).members.add(User.objects.get(pk=1))
		self.client.login(username='testuser', password='password')
		data = {
			'organization': '1',
		}
		resp = self.client.post(reverse('organizations:leave'), data=data)

		org = Organization.objects.get(pk=1)
		self.assertFalse(org.members.filter(username='testuser').exists())

class AutocompleteTest(TestCase):

	fixtures = ['organizations.json']

	# nathan
	def test_post(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('organizations:autocomplete'))
		
		self.assertEqual(resp.status_code, 200)
