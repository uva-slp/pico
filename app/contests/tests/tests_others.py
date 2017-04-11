from django.test import TestCase
from contests.lib import execution as exe
import tempfile
import shutil
import os
from django.core.files import File
from contests.forms import CreateContestForm, CreateContestTemplateForm, CreateProblem, ReturnJudgeResultForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.utils import timezone
from contests.models import Team, Participant, Contest, ContestTemplate, Problem, Submission, ContestInvite
from subprocess import Popen

dir_path = os.path.dirname(os.path.realpath(__file__))


class ContestTemplateTest(TestCase):
    fixtures = ['forms.json']

    # models test
    def contest_template(
            self, title="template test", languages="java, python",
            length=datetime.now(timezone.utc), penalty=datetime.now(timezone.utc), autojudge="1",
            review="Manual review all submissions"):
        return ContestTemplate.objects.create(
            title=title, languages=languages,
            contest_length=length, time_penalty=penalty,
            autojudge_enabled=autojudge, autojudge_review=review)

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
        data = {
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
            desc="problems.pdf"):
        return Contest.objects.create(
            title=title, languages=languages,
            contest_length=length, time_penalty=penalty,
            autojudge_enabled=autojudge, autojudge_review=review,
            problem_description=desc)

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
            self.assertEqual(contest_form.cleaned_data['contest_length'], "02:00")
            self.assertEqual(contest_form.cleaned_data['time_penalty'], "20")

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
            "contest_admins": ct.contest_admins.all(), "contest_participants": ct.contest_participants.all()
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
        data = {"timeout" : 5}
        files = {"solution": SimpleUploadedFile("solution.txt", b"test solution")}
        problem = CreateProblem(data=data, files=files)

        problem1 = problem.save()

        self.assertEqual(problem1.solution.read(), b"test solution")

    # views test
    # Austin
    def test_create_view(self):
        self.client.login(username='judge', password='password')
        url = reverse("contests:create_contest")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)


class JudgeInterfaceTest(TestCase):
    fixtures = ['judge_interface.json']

    # Vivian
    # form test
    def test_valid_return_form_yes(self):
        submission = Submission.objects.get(run_id=3)
        self.assertEqual(str(submission), str(submission.run_id))
        data = {
            "result": "YES", "state": "YES"
        }
        form = ReturnJudgeResultForm(data=data, instance=submission)
        self.assertTrue(isinstance(form.instance, Submission))
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(submission.result, "YES")
        self.assertTrue(submission.state, "YES")

    # Vivian
    # form test
    def test_valid_return_form_no(self):
        submission = Submission.objects.get(run_id=3)
        data = {
            "result": "WRONG", "state": "NO"
        }
        form = ReturnJudgeResultForm(data=data, instance=submission)
        self.assertTrue(isinstance(form.instance, Submission))
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(submission.result, "NO")
        self.assertTrue(submission.state, "NO")


class SubmissionsViewsTest(TestCase):
    fixtures = ['execution.json']

    class Popen_mock_success_1:
        def __init__(self, command, **kwargs):
            self.command = (command.encode(encoding='UTF-8',errors='strict'), ''.encode(encoding='UTF-8',errors='strict'))
            self.returncode = 0
        def communicate(self):
            return self.command
                            
    class Popen_mock_error_1:
        def __init__(self, command, **kwargs):
            self.command = (command.encode(encoding='UTF-8',errors='strict'), 'Compilation Error!'.encode(encoding='UTF-8',errors='strict'))
            self.returncode = 1
        def communicate(self):
            return self.command
    
    class Popen_mock_success_2:
        def __init__(self, command, **kwargs):
            self.command = ('0,' + ' '.join(command), '')
            self.returncode = 0
        def communicate(self):
            return self.command
        
    class Popen_mock_error_2:
        def __init__(self, command, **kwargs):
            self.command = (' '.join(command), 'Docker Error!')
            self.returncode = 1
        def communicate(self):
            return self.command
        
    class Popen_mock_error_3:
        def __init__(self, command, **kwargs):
            self.command = (' '.join(command).encode(encoding='UTF-8',errors='strict'), ''.encode(encoding='UTF-8',errors='strict'))
            self.returncode = 1
        def communicate(self):
            return self.command

    # Derek
    def test_docker_container_code_input_file(self):
        output = exe.docker_container_code(self.Popen_mock_success_1, ['execution.py', 'test.java', '["1","2","3"]', '5', 'input.txt'])
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1], "timeout 5 java -cp code/ test < code/input.txt")

    # Derek
    def test_docker_container_code_bad_file_extension(self):
        output = exe.docker_container_code(self.Popen_mock_success_1, ['execution.py', 'test.banana', '["2","3"]', '5'])
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], "FILENAME ERROR: Must have a valid C++, Java, or Python file extension")

    # Derek
    def test_docker_container_code_java_not_allowed(self):
        output = exe.docker_container_code(self.Popen_mock_success_1, ['execution.py', 'test.java', '["2","3"]', '5'])
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], "LANGUAGE ERROR: Java submissions are not allowed in this contest")

    # Derek
    def test_docker_container_code_cpp_not_allowed(self):
        output = exe.docker_container_code(self.Popen_mock_success_1, ['execution.py', 'test.cpp', '["1","3"]', '5'])
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], "LANGUAGE ERROR: C++ submissions are not allowed in this contest")
        
    # Derek
    def test_docker_container_code__python_not_allowed(self):
        output = exe.docker_container_code(self.Popen_mock_success_1, ['execution.py', 'test.py', '["1","2"]', '5'])
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], "LANGUAGE ERROR: Python submissions are not allowed in this contest")

    # Derek
    def test_docker_container_code_java(self):
        output = exe.docker_container_code(self.Popen_mock_success_1, ['execution.py', 'test.java', '["1","2","3"]', '5'])
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1], "timeout 5 java -cp code/ test")

    # Derek
    def test_docker_container_code_cpp(self):
        output = exe.docker_container_code(self.Popen_mock_success_1, ['execution.py', 'test.cpp', '["1","2","3"]', '5'])
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1], "timeout 5 code/./a.out")
        
    # Derek
    def test_docker_container_code__python(self):
        output = exe.docker_container_code(self.Popen_mock_success_1, ['execution.py', 'test.py', '["1","2","3"]', '5'])
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1], "timeout 5 python code/test.py")
        
    #Derek
    def test_docker_container_code_filename_error(self):
        output = exe.docker_container_code(self.Popen_mock_success_2, ['execution.py', '[1,2,3]', '5'])
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], "FILENAME ERROR: No file name given.")
        
    #Derek
    def test_execute_compiled_file_timeout(self):
        output = exe.execute_compiled_file(self.Popen_mock_error_3, "mock command", None)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], 'CODE TIMED OUT')

    # Derek
    def test_run_java_command_input_file(self):
        output = exe.run_java(self.Popen_mock_success_1, 'trash.java', 'input.txt', 5)
        self.assertEqual(str(output[1]), "timeout 5 java -cp code/ trash < code/input.txt")

    # Derek
    def test_run_cpp_command_input_file(self):
        output = exe.run_cpp(self.Popen_mock_success_1, 'trash.cpp', 'input.txt', 5)
        self.assertEqual(str(output[1]), "timeout 5 code/./a.out < code/input.txt")
        
    # Derek
    def test_run_python_command_input_file(self):
        output = exe.run_python(self.Popen_mock_success_1, 'trash.py', 'input.txt', 5)
        self.assertEqual(str(output[1]), "timeout 5 python code/trash.py < code/input.txt")
                            
    # Derek
    def test_run_java_command_compilation_error(self):
        output = exe.run_java(self.Popen_mock_error_1, 'trash.java', None, 5)
        self.assertEqual(str(output[1]), "COMPILATION ERROR:\nCompilation Error!")

    # Derek
    def test_run_cpp_command_compilation_error(self):
        output = exe.run_cpp(self.Popen_mock_error_1, 'trash.cpp', None, 5)
        self.assertEqual(str(output[1]), "COMPILATION ERROR:\nCompilation Error!")

    # Derek
    def test_run_python_command_execution_error(self):
        output = exe.run_python(self.Popen_mock_error_1, 'trash.py', None, 5)
        self.assertEqual(str(output[1]), "EXECUTION ERROR:\nCompilation Error!")

    # Derek
    def test_run_java_command(self):
        output = exe.run_java(self.Popen_mock_success_1, 'trash.java', None, 5)
        self.assertEqual(str(output[1]), "timeout 5 java -cp code/ trash")

    # Derek
    def test_run_cpp_command(self):
        output = exe.run_cpp(self.Popen_mock_success_1, 'trash.cpp', None, 5)
        self.assertEqual(str(output[1]), "timeout 5 code/./a.out")
        
    # Derek
    def test_run_python_command(self):
        output = exe.run_python(self.Popen_mock_success_1, 'trash.py', None, 5)
        self.assertEqual(str(output[1]), "timeout 5 python code/trash.py")
    
    # Derek
    def test_problem_timeout(self):
        temp_dirpath = tempfile.mkdtemp()
        file_path = os.path.join(temp_dirpath, 'test.cpp')
        problem1 = Problem.objects.get(pk=1)
        problem2 = Problem.objects.get(pk=2)
        with open(file_path, 'w+') as destination:
            test_file_object = File(destination)
            output1 = exe.execute_code(self.Popen_mock_success_2, test_file_object, 'test.cpp', test_file_object, "['1','2','3']", getattr(problem1, 'timeout'))
            output2 = exe.execute_code(self.Popen_mock_success_2, test_file_object, 'test.cpp', test_file_object, "['1','2','3']", getattr(problem2, 'timeout'))
        shutil.rmtree(temp_dirpath)
        self.assertEqual(output1[0], 0)
        self.assertEqual(output1[1][-25:], "['1','2','3'] 7 input.txt")
        self.assertEqual(output2[0], 0)
        self.assertEqual(output2[1][-26:], "['1','2','3'] 20 input.txt")
    
    # Derek
    def test_container_error(self):
        temp_dirpath = tempfile.mkdtemp()
        file_path = os.path.join(temp_dirpath, 'test.cpp')
        problem = Problem.objects.get(pk=1)
        with open(file_path, 'w+') as destination:
            test_file_object = File(destination)
            output = exe.execute_code(self.Popen_mock_error_2, test_file_object, 'test.cpp', test_file_object, "['1','2','3']", getattr(problem, 'timeout'))
        shutil.rmtree(temp_dirpath)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], "CONTAINER ERROR:\nDocker Error!")

    # Derek
    def test_cpp_execution_on_empty_files(self):
        temp_dirpath = tempfile.mkdtemp()
        file_path = os.path.join(temp_dirpath, 'test.cpp')
        with open(file_path, 'w+') as destination:
            test_file_object = File(destination)
            output = exe.execute_code(Popen, test_file_object, 'test.cpp', test_file_object, "['1','2','3']")
        shutil.rmtree(temp_dirpath)
        self.assertEqual(output[0], 1)

    # Derek
    def test_java_execution_on_empty_files(self):
        temp_dirpath = tempfile.mkdtemp()
        file_path = os.path.join(temp_dirpath, 'test.java')
        with open(file_path, 'w+') as destination:
            test_file_object = File(destination)
            output = exe.execute_code(Popen, test_file_object, 'test.java', test_file_object, "['1','2','3']")
        shutil.rmtree(temp_dirpath)
        self.assertEqual(output[0], 1)

    # Derek
    def test_python_execution_on_empty_files(self):
        temp_dirpath = tempfile.mkdtemp()
        file_path = os.path.join(temp_dirpath, 'test.py')
        with open(file_path, 'w+') as destination:
            test_file_object = File(destination)
            output = exe.execute_code(Popen, test_file_object, 'test.py', test_file_object, "['1','2','3']")
        shutil.rmtree(temp_dirpath)
        # An empty file is actually a valid python file, so 0 should be retcode
        self.assertEqual(output[0], 0)

    # Derek
    def test_java_execution_timeout(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "timeout_test.java"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'timeout_test.java', None, "['1','2','3']")
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], "CODE TIMED OUT")  # output[1], code timed out

    # Derek
    def test_cpp_execution_timeout(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "timeout_test.cpp"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'timeout_test.cpp', None, "['1','2','3']")
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], "CODE TIMED OUT")  # output[1], code timed out

    # Derek
    def test_python_execution_timeout(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "timeout_test.py"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'timeout_test.py', None, "['1','2','3']")
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], "CODE TIMED OUT")  # output[1], code timed out

    # Derek
    def test_java_execution_runtime_error(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "runtime_error_test.java"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'runtime_error_test.java', None, "['1','2','3']")
        self.assertEqual(output[0], 1)
        runtime_error = output[1].startswith("EXECUTION ERROR:")
        self.assertEqual(runtime_error, True)  # runtime_error, True

    # Derek
    def test_cpp_execution_runtime_error(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "runtime_error_test.cpp"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'runtime_error_test.cpp', None, "['1','2','3']")
        self.assertEqual(output[0], 1)
        runtime_error = output[1].startswith("EXECUTION ERROR:")
        self.assertEqual(runtime_error, True)

    # Derek
    def test_python_execution_runtime_error(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "runtime_error_test.py"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'runtime_error_test.py', None, "['1','2','3']")
        self.assertEqual(output[0], 1)
        runtime_error = output[1].startswith("EXECUTION ERROR:")
        self.assertEqual(runtime_error, True)

    # Derek
    def test_java_execution_read_input(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "ReadInput.java"), "rb+"))
        input_file = File(open(os.path.join(dir_path, "code_test_files", "input_test_file.txt"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'ReadInput.java', input_file, "['1','2','3']")
        self.assertEqual(output[0], 0)  # output[0], 0
        self.assertEqual(output[1], "The program works!\n")  # output[1], program works

    # Derek
    def test_cpp_execution_read_input(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "ReadInput.cpp"), "rb+"))
        input_file = File(open(os.path.join(dir_path, "code_test_files", "input_test_file.txt"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'ReadInput.cpp', input_file, "['1','2','3']")
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1], "The program works!")

    # Derek
    def test_python_execution_read_input(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "ReadInput.py"), "rb+"))
        input_file = File(open(os.path.join(dir_path, "code_test_files", "input_test_file.txt"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'ReadInput.py', input_file, "['1','2','3']")
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1], "The program works!\n")

    # Derek
    def test_java_execution_no_input(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.java"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.java', None, "['1','2','3']")
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1], "Hello World from Java!\n")

        # Derek

    def test_cpp_execution_no_input(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.cpp"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.cpp', None, "['1','2','3']")
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1], "Hello World from C++!\n")

    # Derek
    def test_python_execution_no_input(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.py"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.py', None, "['1','2','3']")
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1], "Hello World from Python!\n")

    # Derek
    def test_java_execution_compilation_error(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "trash.java"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'trash.java', None, "['1','2','3']")
        self.assertEqual(output[0], 1)
        compilation_error = output[1].startswith("COMPILATION ERROR:")
        self.assertEqual(compilation_error, True)

    # Derek
    def test_cpp_execution_compilation_error(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "trash.cpp"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'trash.cpp', None, "['1','2','3']")
        self.assertEqual(output[0], 1)
        compilation_error = output[1].startswith("COMPILATION ERROR:")
        self.assertEqual(compilation_error, True)

    # Derek
    def test_python_execution_compilation_error(self):
        test_file = File(open(os.path.join(dir_path, "code_test_files", "trash.py"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'trash.py', None, "['1','2','3']")
        self.assertEqual(output[0], 1)
        compilation_error = output[1].startswith("EXECUTION ERROR:")
        self.assertEqual(compilation_error, True)

    # Derek
    def test_execution_contest_no_java_allowed(self):
        allowed_languages = "['2', '3']"
        #Test Java
        test_file_java = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.java"), "rb+"))
        output = exe.execute_code(Popen, test_file_java, 'HelloWorld.java', None, allowed_languages)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1].startswith("LANGUAGE ERROR:"), True)
        #Test C++
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.cpp"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.cpp', None, allowed_languages)
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1].startswith("Hello World"), True)
        #Test Python
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.py"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.py', None, allowed_languages)
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1].startswith("Hello World"), True)

    # Derek
    def test_execution_contest_no_cpp_allowed(self):
        allowed_languages = "['1', '3']"
        #Test Java
        test_file_java = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.java"), "rb+"))
        output = exe.execute_code(Popen, test_file_java, 'HelloWorld.java', None, allowed_languages)
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1].startswith("Hello World"), True)
        #Test C++
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.cpp"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.cpp', None, allowed_languages)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1].startswith("LANGUAGE ERROR:"), True)
        #Test Python
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.py"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.py', None, allowed_languages)
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1].startswith("Hello World"), True)

    # Derek
    def test_execution_contest_no_python_allowed(self):
        allowed_languages = "['1', '2']"
        #Test Java
        test_file_java = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.java"), "rb+"))
        output = exe.execute_code(Popen, test_file_java, 'HelloWorld.java', None, allowed_languages)
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1].startswith("Hello World"), True)
        #Test C++
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.cpp"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.cpp', None, allowed_languages)
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1].startswith("Hello World"), True)
        #Test Python
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.py"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.py', None, allowed_languages)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1].startswith("LANGUAGE ERROR:"), True)

    # Derek
    def test_execution_contest_no_java_cpp_allowed(self):
        allowed_languages = "['3']"
        #Test Java
        test_file_java = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.java"), "rb+"))
        output = exe.execute_code(Popen, test_file_java, 'HelloWorld.java', None, allowed_languages)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1].startswith("LANGUAGE ERROR:"), True)
        #Test C++
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.cpp"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.cpp', None, allowed_languages)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1].startswith("LANGUAGE ERROR:"), True)
        #Test Python
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.py"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.py', None, allowed_languages)
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1].startswith("Hello World"), True)

    # Derek
    def test_execution_contest_no_cpp_python_allowed(self):
        allowed_languages = "['1']"
        #Test Java
        test_file_java = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.java"), "rb+"))
        output = exe.execute_code(Popen, test_file_java, 'HelloWorld.java', None, allowed_languages)
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1].startswith("Hello World"), True)
        #Test C++
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.cpp"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.cpp', None, allowed_languages)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1].startswith("LANGUAGE ERROR:"), True)
        #Test Python
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.py"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.py', None, allowed_languages)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1].startswith("LANGUAGE ERROR:"), True)

    # Derek
    def test_execution_contest_no_java_python_allowed(self):
        allowed_languages = "['2']"
        #Test Java
        test_file_java = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.java"), "rb+"))
        output = exe.execute_code(Popen, test_file_java, 'HelloWorld.java', None, allowed_languages)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1].startswith("LANGUAGE ERROR:"), True)
        #Test C++
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.cpp"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.cpp', None, allowed_languages)
        self.assertEqual(output[0], 0)
        self.assertEqual(output[1].startswith("Hello World"), True)
        #Test Python
        test_file = File(open(os.path.join(dir_path, "code_test_files", "HelloWorld.py"), "rb+"))
        output = exe.execute_code(Popen, test_file, 'HelloWorld.py', None, allowed_languages)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1].startswith("LANGUAGE ERROR:"), True)


# Method for getting nearest datetime
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


class ContestCreationTest(TestCase):
    fixtures = ['users.json', 'teams.json', 'contests.json']
    def setUp(self):
        self.contest_id = 1

    # Jamel
    def testScoreboardConnection(self):
        self.client.login(username='participant1', password='password')

        contest_id = 23
        contest = Contest.objects.get(pk=contest_id)

        url = reverse("contests:scoreboard", kwargs={'contest_id' : 23})

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

    def testScoreboardRefreshConnection(self):
        self.client.login(username='participant1', password='password')

        contest_id = 23
        contest = Contest.objects.get(pk=contest_id)

        url = reverse("contests:refresh_scoreboard")

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

    def testScoreboardFor(self):

        url = reverse("contests:scoreboard", kwargs={'contest_id' : 23})

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

    # Jamel
    def testContestName(self):
        c = Contest(title="testContest")
        c.save()
        contests = Contest.objects.all()
        self.assertEqual(c.title, "testContest")

    # Jamel
    def testContestCreation(self):
        c = Contest(title="super contest")
        self.assertEqual(c.title, "super contest")


class ScoreboardTest(TestCase):
    fixtures = ['users.json', 'teams.json']

    # Jamel
    def testTeamSelection(self):
        ct = Contest()
        ct.save()
        t = Team(name="team1")
        t.save()
        ct.contest_participants.add(t)

        flag = False
        if t in ct.contest_participants.all():
            flag = True

        self.assertTrue(flag)

    # Jamel
    def testParticipants(self):
        ct = Contest()
        t = Team("team1")
        b = Team("team3")
        p1 = Participant(contest=ct, team=t)
        p2 = Participant(contest=ct, team=b)

        self.assertEqual(p1.contest, p2.contest)

    # Jamel
    def testParticipantScore(self):
        ct = Contest()
        t = Team("team1")
        p1 = Participant(contest=ct, team=t)
        p1.score = 5

        self.assertEqual(5, p1.score)

    # Jamel
    def test_participant_creation(self):
        ct = Contest()
        t = Team("team1")
        p = Participant(team=t, contest=ct)
        self.assertTrue(isinstance(p, Participant))

    # Jamel
    def testDate(self):
        requestdatetime = datetime.now(timezone.utc)
        contest = Contest(date_created=datetime.now(timezone.utc))
        nearestdate = []

        nearestdate.append(contest.date_created)

        mostrecentcontestdate = nearest(nearestdate,
                                        requestdatetime)  # Get whatever contest date is nearest to request date
        MRstring = str(mostrecentcontestdate)
        MRstring = MRstring[:-13]
        RDstring = str(requestdatetime)
        RDstring = RDstring[:-13]
        self.assertEqual(RDstring, MRstring)

    # Jamel
    def testContestIDForSubmission(self):
        contest = Contest(id=1)
        contest.save()
        team = Team(name="test")
        contest_id = 1
        contest = Contest.objects.get(id=contest_id)
        testsubmission = Submission(team=team, result="YES")

        self.assertEqual("YES", testsubmission.result)

    # Jamel
    def testContestIDForScoreboard(self):
        contest = Contest(id=1)
        contest.save()
        team = Team(name="test")
        team.save()
        contest_id = 1
        contest = Contest.objects.get(id=contest_id)
        testsubmission = Submission(team=team, result="YES")
        testsubmission.save()
        allsubs = Submission.objects.all()
        allsubs.filter(team=team)
        teststring = allsubs.values_list('result')[0][0]

        self.assertEqual("YES", teststring)

    def testIncorrectTeam(self):
        team1 = Team(name="bob")
        team1.save()
        tempteam = Team.objects.get(name="bob")
        self.assertNotEqual("notbob", team1.name)

    # Jamel
    def testSubmissionPendingStatus(self):
        team = Team(name="test")
        team.save()
        submission = Submission(state="NEW", team=team)
        submission.save()

        allsubs = Submission.objects.all()
        allsubs.filter(team=team)
        pendingstring = allsubs.values_list('state')[0][0]
        self.assertEqual("NEW", pendingstring)

    # Jamel
    def testSelect(self):
        # this test is redundant with testSelectTeam
        ct = Contest()
        ct.save()
        t = Team(name="team1")
        t.save()
        ct.contest_participants.add(t)

        flag = False
        if t in ct.contest_participants.all():
            flag = True

        self.assertTrue(flag)

    # Jamel
    def testScoreboardWrong(self):
        team = Team(name="test")
        team.save()
        submission = Submission(result="WRONG", team=team)
        submission.save()

        allsubs = Submission.objects.all()
        allsubs.filter(team=team)
        wrongstring = allsubs.values_list('result')[0][0]
        self.assertEqual("WRONG", wrongstring)

    # Jamel
    def testScoreboardResultYes(self):
        team = Team(name="test")
        team.save()
        submission = Submission(result="YES", team=team)
        submission.save()

        allsubs = Submission.objects.all()
        allsubs.filter(team=team)
        yesstring = allsubs.values_list('result')[0][0]
        self.assertEqual("YES", yesstring)

    # Jamel
    def testScoreboardResultPending(self):
        team = Team(name="test")
        team.save()
        submission = Submission(result="OFE", team=team)
        submission.save()

        allsubs = Submission.objects.all()
        allsubs.filter(team=team)
        pendingstring = allsubs.values_list('result')[0][0]
        self.assertNotEqual("Pending", pendingstring)

    # Jamel
    def test_participant_false(self):
        ct = Contest()
        t = Team("team1")
        z = Team("team2")
        p = Participant(team=t, contest=ct)
        z = Participant(team=z, contest=ct)
        self.assertFalse(isinstance(z, Team))

    # Jamel
    def testProblemSearchFalse(self):
        t = Team("teamtrue")
        z = Team("teamfalse")
        s = Submission(run_id=1)

        self.assertNotEqual(2, s.run_id)

    # Jamel
    def testProblemSearchTrue(self):
        t = Team("teamtrue")
        z = Team("teamfalse")
        s = Submission(run_id=1)

        self.assertEqual(1, s.run_id)


    # Jamel
    def test_participant_true(self):
        ct = Contest()
        t = Team("team1")
        z = Team("team2")
        p = Participant(team=t, contest=ct)
        z = Participant(team=z, contest=ct)
        self.assertTrue(isinstance(z, Participant))


    # Jamel
    def testTSelect(self):
        # this test is redundant with testSelectTeam and testSelect
        ct = Contest()
        ct.save()
        t = Team(name="team1")
        t.save()
        ct.contest_participants.add(t)

        flag = False
        if t in ct.contest_participants.all():
            flag = True

        self.assertTrue(flag)


    # Jamel
    def testParticipantsAdding(self):
        ct = Contest()
        t = Team("team1")
        b = Team("team3")
        p1 = Participant(contest=ct, team=t)
        p2 = Participant(contest=ct, team=b)

        self.assertEqual(p1.contest, p2.contest)


    # Jamel
    def testParticipantScoreChange(self):
        ct = Contest()
        t = Team("team1")
        p1 = Participant(contest=ct, team=t)
        p1.score = 5

        self.assertEqual(5, p1.score)


    # Jamel
    def testNewTeamFalse(self):
        newTeam = Team(name="banana")
        newTeam.save()
        tempteam = Team.objects.get(name="banana")
        self.assertNotEqual("orange", newTeam.name)


class ContestInvitationTest(TestCase):
    fixtures = ['judge_interface.json']

    # Vivian
    def test_contest_accept_invitation(self):
        self.client.login(username='participant1', password='password')
        contest_id = 7
        contest = Contest.objects.get(pk=contest_id)
        team_id = 1
        team = Team.objects.get(pk=team_id)

        self.assertEqual(len(ContestInvite.objects.all()), 0)
        self.assertEqual(len(contest.participant_set.all()), 0)

        invitation = ContestInvite(contest=contest, team=team)
        invitation.save()
        invitation_id = invitation.id
        self.assertEqual(len(ContestInvite.objects.all()), 1)

        url = reverse("contests:index")
        self.client.post(url, {'accept' : 'Accept', 'invitationId': invitation_id})

        self.assertEqual(len(ContestInvite.objects.all()), 0)
        self.assertEqual(len(contest.participant_set.all()), 1)

    # Vivian
    def test_contest_decline_invitation(self):
        self.client.login(username='participant1', password='password')
        contest_id = 7
        contest = Contest.objects.get(pk=contest_id)
        team_id = 1
        team = Team.objects.get(pk=team_id)

        self.assertEqual(len(ContestInvite.objects.all()), 0)
        self.assertEqual(len(contest.participant_set.all()), 0)

        invitation = ContestInvite(contest=contest, team=team)
        invitation.save()
        invitation_id = invitation.id
        self.assertEqual(len(ContestInvite.objects.all()), 1)

        url = reverse("contests:index")
        self.client.post(url, {'decline' : 'Decline', 'invitationId': invitation_id})

        self.assertEqual(len(ContestInvite.objects.all()), 0)
        self.assertEqual(len(contest.participant_set.all()), 0)
