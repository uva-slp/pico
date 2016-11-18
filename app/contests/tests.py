from django.test import TestCase
from .lib import execution as exe
import tempfile
import shutil
import os
from django.core.files import File
from .forms import CreateContestForm, CreateProblem, ReturnJudgeResultForm
from django.urls import reverse
from django.shortcuts import render
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Team, Participant, Contest, Problem
from datetime import datetime
from django.utils import timezone
from .models import Team, Participant, Contest, Problem, Submission



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

	# Austin
	def test_contest_creation(self):
		ct = self.contest()
		self.assertTrue(isinstance(ct, Contest))
		self.assertEqual(ct.__str__(), ct.title)

	# Austin
	def test_contest_db_entry(self):
		ct = Contest.objects.get(pk=1)
		self.assertEqual(ct.title, 'Contest 1')
		ct.title = "Updated Contest 1"
		ct.save()
		self.assertEqual(ct.title, 'Updated Contest 1')

	# Austin
	def test_problem_creation(self):
		p = Problem(
			solution="solution.txt", input_description="1 2 3 4",
			output_description="5 6 7 8", sample_input="input.txt",
			sample_output="output.txt", contest_id=1)
		p.save()
		self.assertTrue(isinstance(p, Problem))

	# Austin
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
	# Austin
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

	# Austin
	def test_empty_contest_form_fields(self):
		data = {
			"title": "", "languages": "", "contest_length": "",
			"time_penalty": "", "autojudge_enabled": "0", "autojudge_review": "",
			"problem_description": "", "contest_admins": "",
			"contest_participants": ""
		}
		form = CreateContestForm(data=data)
		self.assertFalse(form.is_valid())

	# Austin
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

	# Austin
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

	# Austin
	def test_problem_solution_content(self):
		data = {}
		files = {"solution": SimpleUploadedFile("solution.txt", b"test solution")}
		problem = CreateProblem(data=data, files=files)

		problem1 = problem.save()

		self.assertEqual(problem1.solution.read(), b"test solution")

	# views test
	# Austin
	def test_create_view(self):
		url = reverse("contests:create")
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)


class JudgeInterfaceTest(TestCase):

	fixtures = ['judge_interface.json']

	# Vivian
	#view test
	def test_view_all_judge(self):
		self.client.login(username='judge', password='password')
		url = reverse("contests:contest_judge_submissions",
					  kwargs={'contest_id': 7})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# Vivian
	#view test
	def test_view_all_notloggedin(self):
		url = reverse("contests:contest_judge_submissions",
					  kwargs={'contest_id': 7})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 302)

	# Vivian
	#view test
	def test_view_submission(self):
		self.client.login(username='participant1', password='password')
		url = reverse("contests:contest_submissions",
					  kwargs={'contest_id': 7, 'team_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# Vivian
	#view test
	def test_judge(self):
		self.client.login(username='judge', password='password')
		url = reverse("contests:contest_judge",
					  kwargs={'contest_id': 7, 'run_id': 1})
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

	# Vivian
	#form test
	def test_valid_return_form(self):
		submission = Submission.objects.get(pk=3)
		data = {
			"result": "YES", "state": "YES"
		}
		form = ReturnJudgeResultForm(data=data, instance=submission)
		self.assertTrue(isinstance(form.instance, Submission))
		self.assertTrue(form.is_valid())
		form.save()
		self.assertTrue(submission.result, "YES")
		self.assertTrue(submission.state, "YES")


class SubmissionsViewsTest(TestCase):
	fixtures = ['submission.json']
	
	#Derek
	def test_choose_problem_page(self):
		response = self.client.get(reverse('contests:choose_problem'))
		self.assertEqual(response.status_code, 200)

	#Derek
	def test_choose_problem_page_template(self):
		response = self.client.get(reverse('contests:choose_problem'))
		self.assertTemplateUsed(response, 'contests/choose_problem.html')

	#Derek
	def test_choose_problem_page_title(self):
		response = self.client.get(reverse('contests:choose_problem'))
		self.assertContains(response, 'Problems:')

	#Derek
	def test_upload_code_page(self):
		response = self.client.get(reverse('contests:upload_code', kwargs = {'problem_id': '1'}))
		self.assertEqual(response.status_code, 200)

	#Derek
	def test_upload_code_page_title(self):
		response = self.client.get(reverse('contests:upload_code', kwargs = {'problem_id': '1'}))
		self.assertContains(response, "Submit for ProblemExample")

	#Derek
	def test_cpp_execution_on_empty_file(self):
                temp_dirpath = tempfile.mkdtemp()
                file_path = os.path.join(temp_dirpath, 'test.cpp')
                with open(file_path, 'w+') as destination:
                        test_file_object = File(destination)
                        output = exe.execute_code(test_file_object)
                shutil.rmtree(temp_dirpath)
                self.assertEqual(output[0], 1)
         
    #Derek      
	def test_java_execution_on_empty_file(self):
                temp_dirpath = tempfile.mkdtemp()
                file_path = os.path.join(temp_dirpath, 'test.java')
                with open(file_path, 'w+') as destination:
                        test_file_object = File(destination)
                        output = exe.execute_code(test_file_object)
                shutil.rmtree(temp_dirpath)
                self.assertEqual(output[0], 1)

    #Derek
	def test_diff_with_no_file_template(self):
                response = self.client.get(reverse('contests:diff', kwargs = {'question_id' : '1'}))
                self.assertTemplateUsed(response, 'contests/error.html')

    #Derek
	def test_diff_with_no_file_message(self):
                response = self.client.get(reverse('contests:diff', kwargs = {'question_id' : '1'}))
                self.assertContains(response, 'Invalid form.')

    #Derek
	def test_diff_page(self):
                response = self.client.get(reverse('contests:diff', kwargs = {'question_id' : '1'}))
                self.assertEqual(response.status_code, 200)


# Method for getting nearest datetime
def nearest(items, pivot):
	return min(items, key=lambda x: abs(x - pivot))

class ContestCreationTest(TestCase):
	# Jamel
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
	# Jamel
	def testContestName(self):
		c = Contest(title="testContest")
		c.save()
		contests = Contest.objects.all()
		if(contests.filter(title="testContest")):
			self.assertEqual(c.title, "testContest")
	# Jamel
	def testContestCreation(self):
		c = Contest(title="super contest")
		self.assertEqual(c.title, "super contest")

class ScoreboardTest(TestCase):
	fixtures = ['teams.json']
	# Jamel
	def testTeamSelection(self):

		ct = Contest(contest_participants="team1")
		t = Team(name="team1")

		self.assertEqual(ct.contest_participants, t.name)
	# Jamel
	def testParticipants(self):

		ct = Contest(contest_participants="team1")
		t = Team("team1")
		b = Team("team3")
		p1 = Participant(contest=ct, team=t)
		p2 = Participant(contest=ct, team=b)

		self.assertEqual(p1.contest, p2.contest)
	# Jamel
	def testParticipantScore(self):
		ct = Contest(contest_participants="team1")
		t = Team("team1")
		p1 = Participant(contest=ct, team=t)
		p1.score = 5

		self.assertEqual(5, p1.score)
	# Jamel
	def test_participant_creation(self):
		ct = Contest(contest_participants="team1")
		t = Team("team1")
		p = Participant(team=t, contest=ct)
		self.assertTrue(isinstance(p, Participant))

	# Jamel
	def testDate(self):

		requestdatetime = datetime.now(timezone.utc)
		contest = Contest(date_created=datetime.now(timezone.utc))
		nearestdate = []

		nearestdate.append(contest.date_created)

		mostrecentcontestdate = nearest(nearestdate, requestdatetime)  # Get whatever contest date is nearest to request date
		MRstring = str(mostrecentcontestdate)
		MRstring = MRstring[:-13]
		RDstring = str(requestdatetime)
		RDstring = RDstring[:-13]
		self.assertEqual(RDstring, MRstring)

class CreateContestViewTest(TestCase):

	def test_get(self):
		url = reverse('contests:create')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
