from django.test import TestCase
from django.urls import reverse
from contests.forms import ReturnJudgeResultForm
from contests.models import Team, Participant, Contest, Problem, Submission


class JudgeInterfaceViewTest(TestCase):

	fixtures = ['judge_interface.json']

	# Vivian
	# view test
	def test_view_all_judge(self):
		self.client.login(username='judge', password='password')
		url = reverse("contests:contest_judge_submissions",
					  kwargs={'contest_id': 7})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# Vivian
	# view test
	def test_view_all_notloggedin(self):
		url = reverse("contests:contest_judge_submissions",
					  kwargs={'contest_id': 7})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)

	# Vivian
	# view test
	def test_view_all_nonparticipant(self):
		self.client.login(username='vivianadmin', password='password')
		url = reverse("contests:contest_judge_submissions",
					  kwargs={'contest_id': 7})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)

	# Vivian
	# view test
	def test_view_all_participant(self):
		self.client.login(username='participant1', password='password')
		url = reverse("contests:contest_judge_submissions",
					  kwargs={'contest_id': 7})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)

	# Vivian
	# view test
	def test_view_submission_participant(self):
		self.client.login(username='participant1', password='password')
		url = reverse("contests:contest_submissions",
					  kwargs={'contest_id': 7, 'team_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# Vivian
	# view test
	def test_view_submission_judge(self):
		self.client.login(username='judge', password='password')
		url = reverse("contests:contest_submissions",
					  kwargs={'contest_id': 7, 'team_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# Vivian
	# view test
	def test_view_submission_nonparticipant(self):
		self.client.login(username='vivianadmin', password='password')
		url = reverse("contests:contest_submissions",
					  kwargs={'contest_id': 7, 'team_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)

	# Vivian
	# view test
	def test_view_submission_nonteammember(self):
		self.client.login(username='participant2', password='password')
		url = reverse("contests:contest_submissions",
					  kwargs={'contest_id': 7, 'team_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)

	# Vivian
	# view test
	def test_view_submission_notloggedin(self):
		url = reverse("contests:contest_submissions",
					  kwargs={'contest_id': 7, 'team_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)

	# Vivian
	# view test
	def test_view_judge_judge(self):
		self.client.login(username='judge', password='password')
		url = reverse("contests:contest_judge",
					  kwargs={'contest_id': 7, 'run_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# Vivian
	# view test
	def test_view_judge_participant(self):
		self.client.login(username='participant1', password='password')
		url = reverse("contests:contest_judge",
					  kwargs={'contest_id': 7, 'run_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)

	# Vivian
	# view test
	def test_view_judge_nonparticipant(self):
		self.client.login(username='vivianadmin', password='password')
		url = reverse("contests:contest_judge",
					  kwargs={'contest_id': 7, 'run_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)

	# Vivian
	# view test
	def test_view_judge_notloggedin(self):
		url = reverse("contests:contest_judge",
					  kwargs={'contest_id': 7, 'run_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)
