from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

from users.models import User

class IndexTest(TestCase):

	fixtures = ['users.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')

	# nathan
	def test_user_none(self):
		resp = self.client.get(reverse('users:view'))
		self.assertTemplateUsed(resp, 'users/index.html')
		self.assertIsNone(resp.context['user'])

	# nathan
	def test_user_valid(self):
		resp = self.client.get(reverse('users:view', kwargs={'user_id':1}))
		self.assertTemplateUsed(resp, 'users/index.html')
		self.assertIsNotNone(resp.context['user'])

	# nathan
	def test_user_invalid(self):
		resp = self.client.get(reverse('users:view', kwargs={'user_id':0}))
		self.assertRedirects(resp, reverse('users:view'), 302, 200)

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
			'password1': 'testPassword!',
			'password2': 'testPassword!',
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
		resp = self.client.get(reverse('users:logout'))

		self.assertRedirects(resp, reverse('index'), status_code=302, target_status_code=200)

class EditTest(TestCase):

	fixtures = ['users.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)

	# nathan
	def test_get(self):
		resp = self.client.get(reverse('users:edit'))
		self.assertRedirects(resp, reverse('users:view', kwargs={'user_id':self.user.id}), 302, 200)

	# nathan
	def test_username(self):
		username = 'NEW_USERNAME'
		resp = self.client.post(reverse('users:edit'), data={'username':username})
		user = auth.get_user(self.client)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json()['val'], username)
		self.assertEqual(user.username, username)

	# nathan
	def test_username_in_use(self):
		username = 'admin'
		resp = self.client.post(reverse('users:edit'), data={'username':username})
		self.assertEqual(resp.status_code, 201)
		self.assertTrue('error' in resp.json())

	# nathan
	def test_username_invalid(self):
		username = 'INVALID USERNAME!!!'
		resp = self.client.post(reverse('users:edit'), data={'username':username})
		self.assertEqual(resp.status_code, 201)
		self.assertTrue('error' in resp.json())

	# nathan
	def test_first_name(self):
		first_name = 'James'
		resp = self.client.post(reverse('users:edit'), data={'first_name':first_name})
		user = auth.get_user(self.client)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json()['val'], first_name)
		self.assertEqual(user.first_name, first_name)

	# nathan
	def test_last_name(self):
		last_name = 'James'
		resp = self.client.post(reverse('users:edit'), data={'last_name':last_name})
		user = auth.get_user(self.client)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json()['val'], last_name)
		self.assertEqual(user.last_name, last_name)

	# nathan
	def test_email(self):
		email = 'test@email.com'
		resp = self.client.post(reverse('users:edit'), data={'email':email})
		user = auth.get_user(self.client)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json()['val'], email)
		self.assertEqual(user.email, email)

	# nathan
	def test_email_invalid(self):
		email = 'INVALID EMAIL'
		resp = self.client.post(reverse('users:edit'), data={'email':email})
		self.assertEqual(resp.status_code, 201)
		self.assertTrue('error' in resp.json())

	# nathan
	def test_email_none(self):
		email = ''
		resp = self.client.post(reverse('users:edit'), data={'email':email})
		user = auth.get_user(self.client)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json()['val'], email)
		self.assertEqual(user.email, email)

	# nathan
	def test_theme(self):
		theme = 'http://www.bootstrap-themes.com/example.css'
		resp = self.client.post(reverse('users:edit'), data={'theme':theme})
		user = auth.get_user(self.client)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json()['theme'], theme)
		self.assertEqual(user.profile.theme, theme)

	# nathan
	def test_theme_not_css(self):
		theme = 'http://www.bootstrap-themes.com/example.not_css'
		resp = self.client.post(reverse('users:edit'), data={'theme':theme})
		self.assertEqual(resp.status_code, 201)
		self.assertTrue('error' in resp.json())

	# nathan
	def test_theme_none(self):
		theme = ''
		resp = self.client.post(reverse('users:edit'), data={'theme':theme})
		user = auth.get_user(self.client)
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('theme' in resp.json())
		self.assertEqual(user.profile.theme, theme)

	# nathan
	def test_invalid(self):
		resp = self.client.post(reverse('users:edit'), data={'NOT_A_FIELD':''})
		self.assertEqual(resp.status_code, 400)

class SettingsTest(TestCase):

	fixtures = ['users.json']

	# nathan
	def test_get(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('users:settings'))
		self.assertFalse('disk_usage' in resp.context)

	# nathan
	def test_get_staff(self):
		self.client.login(username='admin', password='admin')
		resp = self.client.get(reverse('users:settings'))
		self.assertTrue('disk_usage' in resp.context)

class AutocompleteTest(TestCase):

	fixtures = ['users.json']

	# nathan
	def test_unauthenticated(self):
		resp = self.client.get(reverse('users:autocomplete'))
		self.assertQuerysetEqual(resp.json()['results'], User.objects.none())

	# nathan
	def test_authenticated(self):
		self.client.login(username='testuser', password='password')
		resp = self.client.get(reverse('users:autocomplete'))
		list1 = [item['text'] for item in resp.json()['results']]
		list2 = [user.username for user in User.objects.all().order_by('id')[:10]]
		self.assertListEqual(list1, list2)

	# nathan
	def test_authenticated_query(self):
		self.client.login(username='testuser', password='password')
		q = 'a'
		resp = self.client.get(reverse('users:autocomplete'), data={'q':q})
		list1 = [item['text'] for item in resp.json()['results']]
		list2 = [user.username for user in User.objects.filter(username__istartswith=q).order_by('id')[:10]]
		self.assertListEqual(list1, list2)

class PasswordChangeTest(TestCase):

	fixtures = ['users.json']

	def setUp(self):
		self.client.login(username='testuser', password='password')
		self.user = auth.get_user(self.client)

	# Vivian
	def test_get(self):
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
