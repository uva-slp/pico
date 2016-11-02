from django.test import TestCase
from .forms import CreateContestTemplate
from .forms import CreateContestForm
from .models import ContestTemplate
from django.urls import reverse
from django.shortcuts import render
from .models import Contest


class ContestTemplateTest(TestCase):

	fixtures = ['forms.json']

	# models test
	def contest_template(
			self, title="only a test", creator="admin", languages="java, python",
			length="02:00", penalty="20", autojudge="0", review="",
			desc="problems.pdf", solution="solutions.txt", admins="",
			participants=""):
		return ContestTemplate.objects.create(
			title=title, creator=creator, languages=languages,
			contest_length=length, time_penalty=penalty,
			autojudge_enabled=autojudge, autojudge_review=review,
			problem_description=desc, solutions=solution,
			contest_admins=admins, contest_participants=participants)

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
		self, title="only a test", creator="admin", languages="Python",
		length="02:00", autojudge="0",
		desc="problems.pdf", solution="solutions.txt", admins="",
		participants=""):
		return Contest.objects.create(
			title=title, creator=creator, languages=languages,
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
		c = Contest(title="super contest", creator="james")
		self.assertEqual(c.title, "super contest")
		self.assertEqual(c.creator, "james")
