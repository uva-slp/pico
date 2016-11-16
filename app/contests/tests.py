from django.test import TestCase
from .forms import CreateContestForm, CreateProblem
from django.urls import reverse
from django.shortcuts import render
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Team, Participant, Contest, Problem


class ContestTest(TestCase):

	fixtures = ['forms.json']

	# models test
	def contest(
			self, title="only a test", languages="java, python",
			length="02:00", penalty="20", autojudge="0", review="",
			desc="problems.pdf", admins="", participants=""):
		return Contest.objects.create(
			title=title, languages=languages,
			contest_length=length, time_penalty=penalty,
			autojudge_enabled=autojudge, autojudge_review=review,
			problem_description=desc, contest_admins=admins,
			contest_participants=participants)

	def test_contest_creation(self):
		ct = self.contest()
		self.assertTrue(isinstance(ct, Contest))
		self.assertEqual(ct.__str__(), ct.title)

	def test_contest_db_entry(self):
		ct = Contest.objects.get(pk=1)
		self.assertEqual(ct.title, 'Contest 1')
		ct.title = "Updated Contest 1"
		ct.save()
		self.assertEqual(ct.title, 'Updated Contest 1')

	def test_problem_creation(self):
		p = Problem(
			solution="solution.txt", input_description="1 2 3 4",
			output_description="5 6 7 8", sample_input="input.txt",
			sample_output="output.txt", contest_id=1)
		p.save()
		self.assertTrue(isinstance(p, Problem))

	def test_problems_in_contest(self):
		ct1 = Contest.objects.get(pk=1)
		ct2 = Contest.objects.get(pk=2)
		ct1.save()
		ct2.save()

		p1 = Problem(
			solution="solution.txt", input_description="1 2 3 4",
			output_description="5 6 7 8", sample_input="input.txt",
			sample_output="output.txt", contest_id=1)
		p2 = Problem(
			solution="solution.txt", input_description="1 2 3 4",
			output_description="5 6 7 8", sample_input="input.txt",
			sample_output="output.txt", contest_id=2)
		p3 = Problem(
			solution="solution.txt", input_description="1 2 3 4",
			output_description="5 6 7 8", sample_input="input.txt",
			sample_output="output.txt", contest_id=1)

		p1.save()
		p2.save()
		p3.save()

		self.assertEqual(Contest.objects.get(pk=p1.contest_id), ct1)
		self.assertEqual(Contest.objects.get(pk=p2.contest_id), ct2)
		self.assertEqual(Contest.objects.get(pk=p3.contest_id), ct1)

	# forms test
	def test_valid_contest_form(self):
		data = {
			"title": "Contest 1", "creator": 1, "languages": "java, python",
			"contest_length": "02:00", "time_penalty": "20",
			"autojudge_enabled": "0", "autojudge_review": "",
			"problem_description": "problems.pdf",
			"contest_admins": "", "contest_participants": ""
		}
		files = {
			"problem_description": SimpleUploadedFile("problems.pdf", b"test content")
		}
		form = CreateContestForm(data=data, files=files)
		self.assertTrue(form.is_valid())

	def test_empty_contest_form_fields(self):
		data = {
			"title": "", "languages": "", "contest_length": "",
			"time_penalty": "", "autojudge_enabled": "0", "autojudge_review": "",
			"problem_description": "", "contest_admins": "",
			"contest_participants": ""
		}
		form = CreateContestForm(data=data)
		self.assertFalse(form.is_valid())

	def test_valid_problem_form(self):
		data = {
			"input_description": "1 2 3 4",
			"output_description": "5 6 7 8",
			"contest": ""
		}
		files = {
			"solution": SimpleUploadedFile("solution.txt", b"test solution"),
			"sample_input": SimpleUploadedFile("input.txt", b"test sample input"),
			"sample_output": SimpleUploadedFile("output.txt", b"test sample output"),
		}
		problem = CreateProblem(data=data, files=files)
		self.assertTrue(problem.is_valid())

	def test_empty_problem_form_fields(self):
		data = {
			"input_description": "",
			"output_description": "",
			"contest": ""
		}
		files = {
			"solution": "",
			"sample_input": "",
			"sample_output": "",
		}
		problem = CreateProblem(data=data, files=files)
		self.assertFalse(problem.is_valid())

	def test_problem_solution_content(self):
		data = {}
		files = {"solution": SimpleUploadedFile("solution.txt", b"test solution")}
		problem = CreateProblem(data=data, files=files)

		problem1 = problem.save()

		self.assertEqual(problem1.solution.read(), b"test solution")

	# views test
	def test_create_view(self):
		url = reverse("contests:create")
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

'''
class ContestTest(TestCase):

	fixtures = ['contests.json']

	# model test
	def contest(
		self, title="only a test", languages="Python",
		length="02:00", autojudge="0",
		desc="problems.pdf", solution="solutions.txt", admins="",
		participants=""):
		return Contest.objects.create(
			title=title, languages=languages,
			contest_length=length,
			autojudge=autojudge, problem_description=desc, 
			solutions=solution, contest_admins=admins, 
			contest_participants=participants)

	def test_contest_creation(self):
		c = Contest()
		c.title = "Contest 1"
		self.assertTrue(isinstance(c, Contest))
		self.assertEqual(c.__str__(), c.title)

	def test_contest_db_entry(self):
		c = Contest.objects.get(pk=1)
		#self.assertEqual(c.title, 'Contest 1')
		c.title = "Updated Contest 1"
		c.save()
		self.assertEqual(c.title, 'Updated Contest 1')

	# forms test
	def test_valid_form(self):
		data = {
			"title": "Contest 1", "languages": "Java, Python",
			"contest_length": "02:00",
			"autojudge": "Jason", "contest_admins": "", 
			"contest_participants": ""
		}
		form = CreateContestForm(data=data)
		self.assertFalse(form.is_valid())

	def test_empty_form_fields(self):
		data = {
			"title": "", "languages": "", "contest_length": "",
			"autojudge": "",
			"contest_admins": "", "contest_participants": ""
		}
		form = CreateContestForm(data=data)
		self.assertFalse(form.is_valid())

	# views test
	def test_create_view(self):
		url = reverse("contests:create")
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)
'''
'''
class SubmissionsViewsTest(TestCase):
	fixtures = ['submission.json']
	
	def test_choose_problem_page(self):
		response = self.client.get(reverse('contests:choose_problem'))
		self.assertEqual(response.status_code, 200)

	def test_choose_problem_page_template(self):
		response = self.client.get(reverse('contests:choose_problem'))
		self.assertTemplateUsed(response, 'contests/choose_problem.html')

	def test_choose_problem_page_title(self):
		response = self.client.get(reverse('contests:choose_problem'))
		self.assertContains(response, 'Problems:')

	def test_upload_code_page(self):
		response = self.client.get(reverse('contests:upload_code', kwargs = {'problem_id': '1'}))
		self.assertEqual(response.status_code, 200)

	def test_upload_code_page_title(self):
		response = self.client.get(reverse('contests:upload_code', kwargs = {'problem_id': '1'}))
		self.assertContains(response, "Submit for ProblemExample")
'''
class ContestCreationTest(TestCase):

	def testNumberofContests(self):
		a = Contest(title="contest1")
		b = Contest(title="contest1")
		c = Contest(title="contest1")
		d = Contest(title="contest1")
		e = Contest(title="contest1")
		a.save()
		b.save()
		c.save()
		d.save()
		e.save()
		contests = Contest.objects.all()
		teamnumber = contests.count()
		self.assertEqual(teamnumber, 5)

	def testContestName(self):
		c = Contest(title="testContest")
		c.save()
		contests = Contest.objects.all()
		if(contests.filter(title="testContest")):
			self.assertEqual(c.title, "testContest")

	def testContestCreation(self):
		c = Contest(title="super contest")
		self.assertEqual(c.title, "super contest")

class ScoreboardTest(TestCase):
	fixtures = ['teams.json']

	def testTeamSelection(self):

		ct = Contest(contest_participants="team1")
		t = Team(name="team1")

		self.assertEqual(ct.contest_participants, t.name)

	def testParticipants(self):

		ct = Contest(contest_participants="team1")
		t = Team("team1")
		b = Team("team3")
		p1 = Participant(contest=ct, team=t)
		p2 = Participant(contest=ct, team=b)

		self.assertEqual(p1.contest, p2.contest)

	def testParticipantScore(self):
		ct = Contest(contest_participants="team1")
		t = Team("team1")
		p1 = Participant(contest=ct, team=t)
		p1.score = 5

		self.assertEqual(5, p1.score)

	def test_participant_creation(self):
		ct = Contest(contest_participants="team1")
		t = Team("team1")
		p = Participant(team=t, contest=ct)
		self.assertTrue(isinstance(p, Participant))

	def team_rankings(self):
		c1 = Contest(contest_participants='team1')
		t1 = Team("team1")
		p1 = Participant(team=t1, contest=c1, score=1)
		t2 = Team("team2")
		p2 = Participant(team=t2, contest=c1, score=2)
		self.assertTrue(p2.score > p1.score)

class CreateContestViewTest(TestCase):

	def test_get(self):
		url = reverse('contests:create')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)

class CreateContestRedirectTest(TestCase):

	def test_submit(self):
		data = {
			"title": "Contest 1", "creator": 1, "languages": "java, python",
			"contest_length": "02:00", "time_penalty": "20",
			"autojudge_enabled": "0", "autojudge_review": "",
			"problem_description": "problems.pdf",
			"contest_admins": "", "contest_participants": ""
		}
		resp = self.client.post(reverse('contests:create'), data=data)
		self.assertRedirects(resp, reverse('contests:home'), status_code=302, target_status_code=200)