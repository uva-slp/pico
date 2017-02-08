from django.urls import reverse
from django.test import TestCase

class RegisterTest(TestCase):

	# nathan
	def test_get(self):
		url = reverse('users:register')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# nathan
	def test_post(self):
		data = {
			'username': 'testuser',
			'password': 'password',
		}
		resp = self.client.post(reverse('users:register'), data=data)

		# self.assertRedirects(resp, reverse('home'), status_code=302, target_status_code=200)
		self.assertRedirects(resp, reverse('home'), status_code=302, target_status_code=302)

class LoginTest(TestCase):

	fixtures = ['users.json']

	# nathan
	def test_get(self):
		url = reverse('users:login')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# nathan
	def test_post(self):
		data = {
			'username': 'testuser',
			'password': 'password',
		}
		resp = self.client.post(reverse('users:login'), data=data)

		# self.assertRedirects(resp, reverse('home'), status_code=302, target_status_code=200)
		self.assertRedirects(resp, reverse('home'), status_code=302, target_status_code=302)

class LogoutTest(TestCase):

	fixtures = ['users.json']
	
	# nathan
	def test_logout(self):
		self.client.login(username='testuser', password='password')
		url = reverse('users:logout')
		resp = self.client.get(url)

		self.assertRedirects(resp, reverse('index'), status_code=302, target_status_code=200)

class PasswordChangeTest(TestCase):

	fixtures = ['users.json']

	# Vivian
	def test_get(self):
		self.client.login(username='testuser', password='password')
		url = reverse('users:password_change')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# nathan
	def test_post(self):
		self.client.login(username='testuser', password='password')
		data = {
			'old_password': 'password',
			'new_password1': 'newpassword',
			'new_password2': 'newpassword'
		}
		resp = self.client.post(reverse('users:password_change'), data=data)

		self.assertEqual(resp.status_code, 302)
		self.assertTrue(self.client.login(username='testuser', password='newpassword'))

class PasswordResetTest(TestCase):

	fixtures = ['users.json']

	# Vivian
	def test_get_form(self):
		url = reverse('users:password_reset')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# Vivian
	def test_get_done(self):
		url = reverse('users:password_reset_done')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# Vivian
	def test_get_complete(self):
		url = reverse('users:password_done')
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# Vivian
	def test_post(self):
		data = {
			'email': 'test@test.com'
		}
		resp = self.client.post(reverse('users:password_reset'), data=data)

		self.assertRedirects(resp, reverse('users:password_reset_done'), status_code=302, target_status_code=200)
