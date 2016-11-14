from django.test import TestCase
from .forms import CreateContestTemplate
from .forms import CreateContestForm
from django.urls import reverse
from django.shortcuts import render
from .lib import execution as exe
import tempfile
import shutil
import os
from django.core.files import File
from .models import Team, Participant, Contest, ContestTemplate


class ContestTemplateTest(TestCase):

	fixtures = ['forms.json']

	# models test
	def contest_template(
			self, title="only a test", languages="java, python",
			length="02:00", penalty="20", autojudge="0", review="",
			desc="problems.pdf", admins="", participants=""):
		return ContestTemplate.objects.create(
			title=title, languages=languages,
			contest_length=length, time_penalty=penalty,
			autojudge_enabled=autojudge, autojudge_review=review,
			problem_description=desc, contest_admins=admins,
			contest_participants=participants)

	def test_contest_template_creation(self):
		ct = self.contest_template()
		self.assertTrue(isinstance(ct, ContestTemplate))
		self.assertEqual(ct.__str__(), ct.title)

	def test_contest_template_db_entry(self):
		ct = ContestTemplate.objects.get(pk=1)
		self.assertEqual(ct.title, 'Contest 1')
		ct.title = "Updated Contest 1"
		ct.save()
		self.assertEqual(ct.title, 'Updated Contest 1')

	# forms test
	def test_valid_form(self):
		data = {
			"title": "Contest 1", "languages": "java, python",
			"contest_length": "02:00", "time_penalty": "20",
			"autojudge_enabled": "0", "autojudge_review": "",
			"contest_admins": "", "contest_participants": ""
		}
		form = CreateContestTemplate(data=data)
		self.assertTrue(form.is_valid())

	def test_empty_form_fields(self):
		data = {
			"title": "", "languages": "", "contest_length": "",
			"time_penalty": "", "autojudge_enabled": "0", "autojudge_review": "",
			"contest_admins": "", "contest_participants": ""
		}
		form = CreateContestTemplate(data=data)
		self.assertFalse(form.is_valid())

	# views test
	def test_create_template_view(self):
		url = reverse("contests:createTemplate")
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)
##
		
class ContestTest(TestCase):

	fixtures = ['contests.json']

	# model test
	def contest_template(
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
##

class SubmissionsViewsTest(TestCase):
	fixtures = ['submission.json']
	
	def test_choose_question_page(self):
		response = self.client.get(reverse('contests:choose_question'))
		self.assertEqual(response.status_code, 200)

	def test_choose_question_page_template(self):
		response = self.client.get(reverse('contests:choose_question'))
		self.assertTemplateUsed(response, 'contests/choose_question.html')
	def test_choose_question_page_title(self):
		response = self.client.get(reverse('contests:choose_question'))
		self.assertContains(response, 'Questions:')

	def test_upload_code_page(self):
		response = self.client.get(reverse('contests:upload_code', kwargs = {'question_id': '1'}))
		self.assertEqual(response.status_code, 200)

	def test_upload_code_page_title(self):
		response = self.client.get(reverse('contests:upload_code', kwargs = {'question_id': '1'}))
		self.assertContains(response, "Submit for QuestionExample")

	def test_cpp_execution_on_empty_file(self):
                temp_dirpath = tempfile.mkdtemp()
                file_path = os.path.join(temp_dirpath, 'test.cpp')
                with open(file_path, 'w+') as destination:
                        test_file_object = File(destination)
                        output = exe.execute_code(test_file_object)
                shutil.rmtree(temp_dirpath)
                self.assertEqual(output[0], 1)
                
	def test_java_execution_on_empty_file(self):
                temp_dirpath = tempfile.mkdtemp()
                file_path = os.path.join(temp_dirpath, 'test.java')
                with open(file_path, 'w+') as destination:
                        test_file_object = File(destination)
                        output = exe.execute_code(test_file_object)
                shutil.rmtree(temp_dirpath)
                self.assertEqual(output[0], 1)

	def test_diff_with_no_file_template(self):
                response = self.client.get(reverse('contests:diff', kwargs = {'question_id' : '1'}))
                self.assertTemplateUsed(response, 'contests/error.html')

	def test_diff_with_no_file_message(self):
                response = self.client.get(reverse('contests:diff', kwargs = {'question_id' : '1'}))
                self.assertContains(response, 'Invalid form.')

	def test_diff_page(self):
                response = self.client.get(reverse('contests:diff', kwargs = {'question_id' : '1'}))
                self.assertEqual(response.status_code, 200)
                
                
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

		ct = ContestTemplate(contest_participants="team1")
		t = Team(name="team1")

		self.assertEqual(ct.contest_participants, t.name)

	def testParticipants(self):

		ct = ContestTemplate(contest_participants="team1")
		t = Team("team1")
		b = Team("team3")
		p1 = Participant(contest=ct, team=t)
		p2 = Participant(contest=ct, team=b)

		self.assertEqual(p1.contest, p2.contest)

	def testParticipantScore(self):
		ct = ContestTemplate(contest_participants="team1")
		t = Team("team1")
		p1 = Participant(contest=ct, team=t)
		p1.score = 5

		self.assertEqual(5, p1.score)

	def test_participant_creation(self):
		ct = ContestTemplate(contest_participants="team1")
		t = Team("team1")
		p = Participant(team=t, contest=ct)
		self.assertTrue(isinstance(p, Participant))
