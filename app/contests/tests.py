from django.test import TestCase
from .forms import CreateContestTemplate
from .models import ContestTemplate
from django.urls import reverse


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
