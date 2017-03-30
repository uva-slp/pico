from django.shortcuts import reverse
from django.test import TestCase

class WsgiTest(TestCase):

    # nathan
    def test_wsgi(self):
        from pico import wsgi

class PicoTest(TestCase):
    

    fixtures = ['users.json']

    # nathan
    def test_anonymous_required_anon(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    # nathan
    def test_anonymous_required(self):
        self.client.login(username='testuser', password='password')
        resp = self.client.get(reverse('index'))
        self.assertRedirects(resp, reverse('home'), status_code=302, target_status_code=302)
