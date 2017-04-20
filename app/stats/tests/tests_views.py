from django.contrib import auth
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from contests.models import Team, Contest, Problem, Participant,Submission
from datetime import datetime


class DisplayContestTest(TestCase):
    fixtures = ['users.json', 'teams.json', 'contests.json', 'problems.json']

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

        test_contest = Contest.objects.get(id=22)
        test_team = Team.objects.get(id=3)
        participant = Participant(contest=test_contest, team=test_team)
        participant.save()
        problem = Problem.objects.get(id=1)
        test_submission = Submission(run_id=1, team=test_team, problem=problem, timestamp=datetime.now(timezone.utc), state="YES", result="YES")
        test_submission.save()

        url = reverse("stats:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


