from django.contrib import auth
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from contests.forms import ReturnJudgeResultForm, CreateContestForm, CreateContestTemplateForm, CreateProblem
from contests.models import Team, Participant, Contest, Problem, Submission, ContestTemplate
from contests.views import create, edit, create_new_problem


class ContestViewTest(TestCase):

    fixtures = ['judge_interface.json']

    # Vivian
    def test_view_contest_judge(self):
        self.client.login(username='judge', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest", kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_contest_admin(self):
        self.client.login(username='myadmin', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest", kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_contest_participant(self):
        self.client.login(username='participant1', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        test_contest = Contest.objects.get(id=7)
        test_team = Team.objects.get(id=1)
        participant = Participant(contest=test_contest, team=test_team)
        participant.save()
        url = reverse("contests:contest", kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_contest_superuser(self):
        self.client.login(username='admin', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest", kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_contest_nonparticipant(self):
        self.client.login(username='nonparticipant', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest", kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)


    # Vivian
    def test_view_contest_nonloggedin(self):
        url = reverse("contests:contest", kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)


class JudgeInterfaceViewTest(TestCase):

    fixtures = ['judge_interface.json']

    # Vivian
    def test_view_all_judge(self):
        self.client.login(username='judge', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_judge_submissions",
                      kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_all_judge(self):
        self.client.login(username='myadmin', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_judge_submissions",
                      kwargs={'contest_id': 7})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_all_notloggedin(self):
        url = reverse("contests:contest_judge_submissions",
                      kwargs={'contest_id': 7})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_all_nonparticipant(self):
        self.client.login(username='myadmin', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_judge_submissions",
                      kwargs={'contest_id': 7})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_all_participant(self):
        self.client.login(username='participant1', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_judge_submissions",
                      kwargs={'contest_id': 7})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_submission_participant(self):
        self.client.login(username='participant1', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_submissions",
                      kwargs={'contest_id': 7, 'team_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_submission_judge(self):
        self.client.login(username='judge', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_submissions",
                      kwargs={'contest_id': 7, 'team_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_submission_nonparticipant(self):
        self.client.login(username='myadmin', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_submissions",
                      kwargs={'contest_id': 7, 'team_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_submission_nonteammember(self):
        self.client.login(username='participant2', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_submissions",
                      kwargs={'contest_id': 7, 'team_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_submission_notloggedin(self):
        url = reverse("contests:contest_submissions",
                      kwargs={'contest_id': 7, 'team_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_judge_judge(self):
        self.client.login(username='judge', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_judge",
                      kwargs={'contest_id': 7, 'run_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_judge_participant(self):
        self.client.login(username='participant1', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_judge",
                      kwargs={'contest_id': 7, 'run_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_judge_nonparticipant(self):
        self.client.login(username='myadmin', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_judge",
                      kwargs={'contest_id': 7, 'run_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_judge_notloggedin(self):
        url = reverse("contests:contest_judge",
                      kwargs={'contest_id': 7, 'run_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)


class LoadTemplateTest(TestCase):

    fixtures = ['users.json', 'forms.json']

    # Austin
    def test_load_valid_template(self):
        self.client.login(username='testuser', password='password')

        data = {"selected_template": 1, "submit": "load_template"}
        resp = self.client.post(reverse('contests:create'), data=data)
        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_redirect_create_template_page(self):
        self.client.login(username='testuser', password='password')

        resp = self.client.get(reverse('contests:create_template'))
        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_create_template(self):
        self.client.login(username='testuser', password='password')

        data = {
            "title": "Contest test 1", "languages": "java, python",
            "contest_length": "02:00", "time_penalty": "20",
            "autojudge_enabled": "0", "autojudge_review": "",
            "contest_admins": "", "contest_participants": ""
        }
        resp = self.client.post(reverse('contests:create_template'), follow=True, data=data)
        self.assertEqual(resp.status_code, 200)


class ModifyContestViewTest(TestCase):

    fixtures = ['users.json', 'forms.json']

    # Austin
    def test_create_contest(self):
        self.client.login(username='testuser', password='password')

        data = {
            "title": "Contest test 1", "creator": 1, "languages": "java, python",
            "contest_length": "02:00", "time_penalty": "20",
            "autojudge_enabled": "0", "autojudge_review": "",
            "problem_description": "problems.pdf",
            "contest_admins": "", "contest_participants": "",
            "submit": "create_contest",
            "form-TOTAL_FORMS": 1, "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 0, "form-MAX_NUM_FORMS": 1000
        }
        resp = self.client.post(reverse('contests:create'), data=data)
        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_edit_view(self):
        self.client.login(username='testuser', password='password')

        resp = self.client.get(reverse('contests:edit_contest', kwargs={'contest_id': 7}))
        self.assertNotEqual(resp.status_code, 200)

    '''
    #@mock.patch('contests.views.messages')
    #@mock.patch('contests.views.forms.CreateProblemForm')
    def test_create_new_problem(self):
        self.client.login(username='testuser', password='password')
        data = {}
        files = {"solution": SimpleUploadedFile("solution.txt", b"test solution")}
        problem = CreateProblem(data=data, files=files)
        request = self.client.get(reverse("contests:edit_contest", kwargs={'contest_id': 7}))
        if problem.is_valid():
            problem = problem.cleaned_data
            response = create_new_problem(request, problem, 25, 7)
            messages = list(response.context['messages'])
            messages.success(self.request._request, "New problem created")
            #self.assertEqual(len(messages), 1)
        #self.assertTrue(Problem.objects.get(contest_id=7))
        #self.request = RequestFactory()
        #request = self.client.get(reverse("contests:edit_contest", kwargs={'contest_id': 7}))
        #request.POST['submit'] = 'save_new_problem'
        #request.user = auth.get_user(self.client)
        #response = edit(request, 1)
        #response = self.client.post(reverse("contests:edit", data=problem)
        #self.assertEqual(response.status_code, 404)
        #request = RequestFactory().post(reverse("contests:edit", kwargs={'contest_id': 7}), problem)
        #response = create(request)
        problem_form = form_class.return_value
        problem_form.is_valid.return_value = True
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/edit/7')
        problem_form.save.assert_called()  # test that save() is called
        messages.info.assert_called_with(request, 'New problem created')
        #problem1 = problem.save()
        #url = reverse("contests:edit", kwargs={'contest_id': 7})
        #resp = self.client.post(url, problem)
        #self.assertEqual(resp.status_code, 302)
        #self.assertEqual(problem1.solution.read(), b"test solution")'''

    # Austin
    def test_invalid_user_edit_contest(self):
        self.client.login(username='testuser', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:edit_contest", kwargs={'contest_id': 7})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    # Austin
    def test_valid_user_edit_contest(self):
        self.client.login(username='testuser', password='password')
        user = auth.get_user(self.client)
        #print user.id
        assert user.is_authenticated()

        url = reverse("contests:edit_contest", kwargs={'contest_id': 11})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_new_problem_edit(self):
        data = {"submit": "save_new_problem"}
        resp = self.client.post(reverse("contests:edit_contest", kwargs={'contest_id': 11}), follow=True, data=data)
        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_delete_problem_edit(self):
        data = {"submit": "delete_problem"}
        resp = self.client.post(reverse("contests:edit_contest", kwargs={'contest_id': 11}), follow=True, data=data)
        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_update_problem_edit(self):
        data = {"submit": "update_problem"}
        resp = self.client.post(reverse("contests:edit_contest", kwargs={'contest_id': 11}), follow=True, data=data)
        self.assertEqual(resp.status_code, 200)
