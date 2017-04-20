from django.contrib import auth
from django.test import TestCase, RequestFactory
from django.urls import reverse


class DisplayContestTest(TestCase):
    fixtures = ['users.json', 'teams.json', 'contests.json']

    def setUp(self):
        self.factory = RequestFactory()

    # Vivian
    def test_view_stat_notloggedin(self):
        url = reverse("stats:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_stat_participant(self):
        self.client.login(username='participant1', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("stats:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


