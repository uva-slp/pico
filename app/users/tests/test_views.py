from django.urls import reverse
from django.test import TestCase

class RegisterTest(TestCase):

	def test_get(self):
		url = reverse('users:register')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	def test_post(self):
		data = {
			'username': 'testuser',
			'password': 'password',
		}
		resp = self.client.post(reverse('users:register'), data=data)

		self.assertRedirects(resp, reverse('contests:home'), status_code=302, target_status_code=200)

class LoginTest(TestCase):

	fixtures = ['users.json']

	def test_get(self):
		url = reverse('users:login')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	def test_post(self):
		data = {
			'username': 'testuser',
			'password': 'password',
		}
		resp = self.client.post(reverse('users:login'), data=data)

		self.assertRedirects(resp, reverse('contests:home'), status_code=302, target_status_code=200)

class LogoutTest(TestCase):

	fixtures = ['users.json']
	
	def test_logout(self):
		self.client.login(username='testuser', password='password')
		url = reverse('users:logout')
		resp = self.client.get(url)

		self.assertRedirects(resp, reverse('index'), status_code=302, target_status_code=200)
