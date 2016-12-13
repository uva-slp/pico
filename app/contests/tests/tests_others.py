from django.test import TestCase
from contests.lib import execution as exe
import tempfile
import shutil
import os
from django.core.files import File
from contests.forms import CreateContestForm, CreateContestTemplateForm, CreateProblem, ReturnJudgeResultForm
from django.urls import reverse
from django.shortcuts import render
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.utils import timezone
from contests.models import Team, Participant, Contest, ContestTemplate, Problem, Submission

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class ContestTemplateTest(TestCase):

	fixtures = ['forms.json']

	# models test
	def contest_template(
			self, title="template test", languages="java, python",
			length=datetime.now(timezone.utc), penalty=datetime.now(timezone.utc), autojudge="1",
			review="Manual review all submissions", admins="", participants=""):
		return ContestTemplate.objects.create(
			title=title, languages=languages,
			contest_length=length, time_penalty=penalty,
			autojudge_enabled=autojudge, autojudge_review=review,
			contest_admins=admins, contest_participants=participants)

	# Austin
	def test_contest_template_creation(self):
		ct = self.contest_template()
		self.assertTrue(isinstance(ct, ContestTemplate))
		self.assertEqual(ct.__str__(), ct.title)

	# Austin
	def test_contest_template_db_entry(self):
		ct = ContestTemplate.objects.get(pk=1)
		self.assertEqual(ct.title, 'Contest from template 1')
		ct.title = "Updated Contest from template 1"
		ct.save()
		updated_ct = ContestTemplate.objects.get(pk=1)
		self.assertEqual(updated_ct.title, 'Updated Contest from template 1')

	# forms test
	def contesttemplate_form(self):
		data={
			"title": "Contest Template 1", "creator": 1, "languages": "java, c++",
			"contest_length": "03:00", "time_penalty": "30",
			"autojudge_enabled": "1", "autojudge_review": "Manual review all submissions",
			"contest_admins": "", "contest_participants": ""
		}
		return CreateContestTemplateForm(data=data)

	# Austin
	def test_valid_contesttemplate_form(self):
		form = self.contesttemplate_form()
		self.assertTrue(form.is_valid())

	# Austin
	def test_empty_contesttemplate_form_fields(self):
		data = {
			"title": "", "languages": "", "contest_length": "",
			"time_penalty": "", "autojudge_enabled": "0", "autojudge_review": "",
			"contest_admins": "", "contest_participants": ""
		}
		form = CreateContestTemplateForm(data=data)
		self.assertFalse(form.is_valid())

class ContestTest(TestCase):

	fixtures = ['judge_interface.json', 'forms.json']

	# models test
	def contest(
			self, title="contest test", languages="java, python",
			length=datetime.now(timezone.utc), penalty=datetime.now(timezone.utc), autojudge="0", review="",
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
		ct = Contest.objects.get(pk=8)
		self.assertEqual(ct.title, 'Contest 1')
		ct.title = "Updated Contest 1"
		ct.save()
		updated_ct = Contest.objects.get(pk=8)
		self.assertEqual(updated_ct.title, 'Updated Contest 1')

	# Austin
	def test_contest_cleaned_datetime(self):
		contest_form = self.contest_form()
		if contest_form.is_valid():
			self.assertNotEqual(contest_form.cleaned_data['contest_length'], "02:00")
			self.assertNotEqual(contest_form.cleaned_data['time_penalty'], "20")

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
	def contest_form(self):
		data={
			"title": "Contest 1", "creator": 1, "languages": "java, python",
			"contest_length": "02:00", "time_penalty": "20",
			"autojudge_enabled": "0", "autojudge_review": "",
			"problem_description": "problems.pdf",
			"contest_admins": "", "contest_participants": ""
		}
		files = {
			"problem_description": SimpleUploadedFile("problems.pdf", b"test content")
		}
		return CreateContestForm(data=data, files=files)

	# Austin
	def test_valid_contest_form(self):
		form = self.contest_form()
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
	def test_valid_contest_from_template(self):
		ct = ContestTemplate.objects.get(pk=1)

		loaded_data = {
			"title": ct.title, "creator": 1, "languages": ct.languages,
			"contest_length": ct.contest_length, "time_penalty": ct.time_penalty,
			"autojudge_enabled": ct.autojudge_enabled, "autojudge_review": ct.autojudge_review,
			"problem_description": "problems.pdf",
			"contest_admins": ct.contest_admins, "contest_participants": ct.contest_participants
		}

		files = {
			"problem_description": SimpleUploadedFile("problems.pdf", b"test content")
		}

		form = CreateContestForm(data=loaded_data, files=files)
		self.assertTrue(form.is_valid())

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
		self.client.login(username='judge', password='password')
		url = reverse("contests:create")
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)

class JudgeInterfaceTest(TestCase):

	fixtures = ['judge_interface.json']

	# Vivian
	# form test
	def test_valid_return_form(self):
		submission = Submission.objects.get(run_id=3)
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
	def test_cpp_execution_on_empty_files(self):
		temp_dirpath = tempfile.mkdtemp()
		file_path = os.path.join(temp_dirpath, 'test.cpp')
		with open(file_path, 'w+') as destination:
			test_file_object = File(destination)
			output = exe.execute_code(test_file_object, 'test.cpp', test_file_object)
		shutil.rmtree(temp_dirpath)
		self.assertEqual(output[0], 1)
	 
    #Derek	
	def test_java_execution_on_empty_files(self):
		temp_dirpath = tempfile.mkdtemp()
		file_path = os.path.join(temp_dirpath, 'test.java')
		with open(file_path, 'w+') as destination:
			test_file_object = File(destination)
			output = exe.execute_code(test_file_object, 'test.java', test_file_object)
		shutil.rmtree(temp_dirpath)
		self.assertEqual(output[0], 1)

    #Derek
	def test_diff_with_no_file_template(self):
		response = self.client.get(reverse('contests:diff', kwargs = {'problem_id' : '1'}))
		self.assertTemplateUsed(response, 'contests/error.html')
		
    #Derek
	def test_diff_with_no_file_message(self):
		response = self.client.get(reverse('contests:diff', kwargs = {'problem_id' : '1'}))
		self.assertContains(response, 'Invalid form.')

    #Derek
	def test_diff_page(self):
		response = self.client.get(reverse('contests:diff', kwargs = {'problem_id' : '1'}))
		self.assertEqual(response.status_code, 200)

    #Derek	
	def test_java_execution_timeout(self):
		test_file = File(open(os.path.join(dir_path, "code_test_files", "timeout_test.java"), "rb+"))
		output = exe.execute_code(test_file, 'timeout_test.java', None)
		self.assertEqual(output[0], 1)
		self.assertEqual(output[1], "Code timed out")

    #Derek      
	def test_cpp_execution_timeout(self):
		test_file = File(open(os.path.join(dir_path, "code_test_files", "timeout_test.cpp"), "rb+"))
		output = exe.execute_code(test_file, 'timeout_test.cpp', None)
		self.assertEqual(output[0], 1)
		self.assertEqual(output[1], "Code timed out")

    #Derek      
	def test_java_execution_runtime_error(self):
		test_file = File(open(os.path.join(dir_path, "code_test_files", "runtime_error_test.java"), "rb+"))
		output = exe.execute_code(test_file, 'runtime_error_test.java', None)
		self.assertEqual(output[0], 1)
		runtime_error = output[1].startswith("EXECUTION ERROR:")
		self.assertEqual(runtime_error, True)
		
    #Derek	
	#def test_cpp_execution_runtime_error(self):
	#	test_file = File(open(os.path.join(dir_path, "code_test_files", "runtime_error_test.cpp"), "rb+"))
	#	output = exe.execute_code(test_file, 'runtime_error_test.cpp', None)
	#	self.assertEqual(output[0], 1)
	#	runtime_error = output[1].startswith("EXECUTION ERROR:")
	#	self.assertEqual(runtime_error, True)

    #Derek      
	def test_java_execution_read_input(self):
		test_file = File(open(os.path.join(dir_path, "code_test_files", "ReadInput.java"), "rb+"))
		input_file = File(open(os.path.join(dir_path, "code_test_files", "input_test_file.txt"), "rb+"))
		output = exe.execute_code(test_file, 'ReadInput.java', input_file)
		self.assertEqual(output[0], 0)
		self.assertEqual(output[1], "The program works!\n")

    #Derek      
	def test_cpp_execution_read_input(self):
		test_file = File(open(os.path.join(dir_path, "code_test_files", "ReadInput.cpp"), "rb+"))
		input_file = File(open(os.path.join(dir_path, "code_test_files", "input_test_file.txt"), "rb+"))
		output = exe.execute_code(test_file, 'ReadInput.cpp', input_file)
		self.assertEqual(output[0], 0)
		self.assertEqual(output[1], "The program works!")

    #Derek      
	def test_java_execution_compilation_error(self):
		test_file = File(open(os.path.join(dir_path, "code_test_files", "trash.java"), "rb+"))
		output = exe.execute_code(test_file, 'trash.java', None)
		self.assertEqual(output[0], 1)
		compilation_error = output[1].startswith("COMPILATION ERROR:")
		self.assertEqual(compilation_error, True)

    #Derek      
	def test_cpp_execution_compilation_error(self):
		test_file = File(open(os.path.join(dir_path, "code_test_files", "trash.cpp"), "rb+"))
		output = exe.execute_code(test_file, 'trash.cpp', None)
		self.assertEqual(output[0], 1)
		compilation_error = output[1].startswith("COMPILATION ERROR:")
		self.assertEqual(compilation_error, True)

                
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

'''
class CreateContestViewTest(TestCase):

	def test_get(self):
		url = reverse('contests:create')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
'''
