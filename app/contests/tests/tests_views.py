from django.contrib import auth
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template import Context, Template
from django.utils import timezone
from contests.models import Team, Participant, Contest, Problem, ContestTemplate, ContestInvite, Submission, Notification
from contests.views import createContest, editContest, createTemplate, activateContest
from datetime import datetime, timedelta, time


class DisplayIndexViewTest(TestCase):
    fixtures = ['users.json', 'teams.json', 'contests.json']

    def setUp(self):
        self.factory = RequestFactory()

    # Vivian
    def test_view_index_notloggedin(self):
        url = reverse("contests:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_index(self):
        self.client.login(username='testuser', password='password')
        url = reverse("contests:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_index_activate(self):
        self.client.login(username='testuser', password='password')
        self.user = auth.get_user(self.client)

        all_active_contest = Contest.objects.active()
        self.assertEqual(len(all_active_contest), 0)

        contest_id = 22

        contest = Contest.objects.get(pk=contest_id)
        self.assertIsNone(contest.contest_start)
        request = self.factory.post(reverse("contests:activate_contest", kwargs={'contest_id': contest_id}))
        request.user = self.user

        resp = activateContest(request, contest_id)
        self.assertEqual(resp.status_code, 302)

        contest.refresh_from_db()
        self.assertIsNotNone(contest.contest_start)

        all_active_contest = Contest.objects.active()
        self.assertEqual(len(all_active_contest), 1)

        url = reverse("contests:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_index_past(self):
        self.client.login(username='testuser', password='password')
        all_active_contest = Contest.objects.active()
        self.assertEqual(len(all_active_contest), 0)

        contest_id = 22

        contest = Contest.objects.get(pk=contest_id)
        self.assertIsNone(contest.contest_start)

        contest.contest_start = datetime.now(timezone.utc) - timedelta(hours=2, minutes=15)
        self.assertIsNotNone(contest.contest_start)
        contest.contest_length = time(hour=2)
        self.assertTrue(contest.contest_end() < datetime.now(timezone.utc))

        contest.save()
        all_past_contest = Contest.objects.past()
        self.assertEqual(len(all_past_contest), 1)

        url = reverse("contests:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_index_invitation(self):
        self.client.login(username='participant1', password='password')
        all_active_contest = Contest.objects.active()
        self.assertEqual(len(all_active_contest), 0)

        test_contest = Contest.objects.get(id=7)
        test_team = Team.objects.get(id=3)
        contest_invite = ContestInvite(contest=test_contest, team=test_team)
        contest_invite.save()
        all_contest_invite = ContestInvite.objects.all()
        self.assertEqual(len(all_contest_invite), 1)

        url = reverse("contests:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)



class DisplayContestViewTest(TestCase):

    fixtures = ['users.json', 'teams.json', 'contests.json', 'problems.json']

    def setUp(self):
        self.factory = RequestFactory()

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
        test_team = Team.objects.get(id=3)
        participant = Participant(contest=test_contest, team=test_team)
        participant.save()
        url = reverse("contests:contest", kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_contest_superuser(self):
        self.client.login(username='admin', password='admin')
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

    # Vivian
    def test_view_contest_with_problems(self):
        self.client.login(username='participant1', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        test_contest = Contest.objects.get(id=22)
        test_team = Team.objects.get(id=3)
        participant = Participant(contest=test_contest, team=test_team)
        participant.save()
        problems = test_contest.problem_set.all()
        problem = list(problems)[0]
        self.assertEqual(len(problems), 2)

        url = reverse("contests:contest", kwargs={'contest_id': 22})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_contest_with_correct_submission(self):
        self.client.login(username='participant1', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        test_contest = Contest.objects.get(id=22)
        test_team = Team.objects.get(id=3)
        participant = Participant(contest=test_contest, team=test_team)
        participant.save()
        problems = test_contest.problem_set.all()
        problem = list(problems)[0]
        self.assertEqual(len(problems), 2)
        test_submission = Submission(run_id=1, team=test_team, problem=problem, timestamp=datetime.now(timezone.utc), state="YES", result="YES")
        test_submission.save()

        url = reverse("contests:contest", kwargs={'contest_id': 22})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_contest_with_unhandled_submission(self):
        self.client.login(username='participant1', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        test_contest = Contest.objects.get(id=22)
        test_team = Team.objects.get(id=3)
        participant = Participant(contest=test_contest, team=test_team)
        participant.save()
        problems = test_contest.problem_set.all()
        problem = list(problems)[0]
        self.assertEqual(len(problems), 2)
        test_submission = Submission(run_id=1, team=test_team, problem=problem, timestamp=datetime.now(timezone.utc), state="NEW")
        test_submission.save()

        url = reverse("contests:contest", kwargs={'contest_id': 22})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_contest_with_wrong_submission(self):
        self.client.login(username='participant1', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        test_contest = Contest.objects.get(id=22)
        test_team = Team.objects.get(id=3)
        participant = Participant(contest=test_contest, team=test_team)
        participant.save()
        problems = test_contest.problem_set.all()
        problem = list(problems)[0]
        self.assertEqual(len(problems), 2)
        test_submission = Submission(run_id=1, team=test_team, problem=problem, timestamp=datetime.now(timezone.utc), state="NO", result="WRONG")
        test_submission.save()

        url = reverse("contests:contest", kwargs={'contest_id': 22})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_activate_contest(self):
        self.client.login(username='testuser', password='password')
        self.user = auth.get_user(self.client)

        contest_id = 22

        contest = Contest.objects.get(pk=contest_id)
        self.assertIsNone(contest.contest_start)

        request = self.factory.post(reverse("contests:activate_contest", kwargs={'contest_id': contest_id}))
        request.user = self.user

        resp = activateContest(request, contest_id)
        self.assertEqual(resp.status_code, 302)

        contest.refresh_from_db()
        self.assertIsNotNone(contest.contest_start)


class JudgeInterfaceViewTest(TestCase):

    fixtures = ['judge_interface.json']

    # Vivian
    def test_view_all_judge(self):
        self.client.login(username='judge', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        test_contest = Contest.objects.get(id=7)
        test_team = Team.objects.get(id=1)
        participant = Participant(contest=test_contest, team=test_team)
        participant.save()
        problems = test_contest.problem_set.all()
        problem = list(problems)[0]
        test_submission = Submission(run_id=1, team=test_team, problem=problem, timestamp=datetime.now(timezone.utc), state="NEW")
        test_submission.save()

        url = reverse("contests:contest_judge_submissions",
                      kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_all_superuser(self):
        self.client.login(username='admin', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_judge_submissions",
                      kwargs={'contest_id': 7})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

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

        self.assertEqual(resp.status_code, 200)

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
    def test_view_submission_superuser(self):
        self.client.login(username='admin', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:contest_submissions",
                      kwargs={'contest_id': 7, 'team_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_submission_nonparticipant(self):
        self.client.login(username='nonparticipant', password='password')
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
    def test_view_judge_superuser(self):
        self.client.login(username='admin', password='password')
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

        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_judge_notloggedin(self):
        url = reverse("contests:contest_judge",
                      kwargs={'contest_id': 7, 'run_id': 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_judge_return_result(self):
        self.client.login(username='judge', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        data = {"result": "YES", "submit": "Submit"}
        resp = self.client.post(reverse("contests:contest_judge", kwargs={'contest_id': 7, 'run_id': 1}),
                                data=data)
        self.assertEqual(resp.status_code, 200)


class DisplayProblemDescriptionViewTest(TestCase):
    fixtures = ['users.json', 'teams.json', 'contests.json']

    def setUp(self):
        self.factory = RequestFactory()

    # Vivian
    def test_view_problem_description_admin(self):
        self.client.login(username='myadmin', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()
        contest = Contest.objects.get(pk=7)
        contest.problem_description = SimpleUploadedFile("foo.txt", b"foo")
        contest.save()
        url = reverse("contests:problem_description", kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # Vivian
    def test_view_problem_description_participant_notactive(self):
        self.client.login(username='participant1', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        url = reverse("contests:problem_description", kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    # Vivian
    def test_view_problem_description_nonparticipant_active(self):
        self.client.login(username='nonparticipant', password='password')
        user = auth.get_user(self.client)
        assert user.is_authenticated()

        contest = Contest.objects.get(pk=7)
        self.assertIsNone(contest.contest_start)

        contest.contest_start = datetime.now(timezone.utc)
        self.assertIsNotNone(contest.contest_start)
        contest.contest_length = time(hour=2)
        self.assertTrue(contest.contest_end() > datetime.now(timezone.utc))

        contest.save()
        all_active_contest = Contest.objects.active()
        self.assertEqual(len(all_active_contest), 1)

        url = reverse("contests:problem_description", kwargs={'contest_id': 7})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)


class LoadTemplateViewTest(TestCase):

    fixtures = ['users.json', 'contest_templates.json']

    def setUp(self):
        # Every test needs access to the request factory and authorized user
        self.factory = RequestFactory()
        self.client.login(username='testuser', password='password')
        self.user = auth.get_user(self.client)

    # Austin
    def test_load_valid_template(self):
        data = {"selected_template": 1, "submit": "load_template"}
        resp = self.client.post(reverse('contests:create_contest'), data=data)
        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_load_invalid_template(self):
        data = {"selected_template": 9999, "submit": "load_template"}
        resp = self.client.post(reverse('contests:create_contest'), data=data)
        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_redirect_create_template_page(self):
        resp = self.client.get(reverse('contests:create_template'))
        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_create_valid_template(self):
        data = {
            "title": "Contest test 1", "languages": "java, python",
            "contest_length": "02:00", "time_penalty": "20",
            "autojudge_enabled": "0", "autojudge_review": "",
        }

        request = self.factory.post(reverse('contests:create_template'), data)
        request.user = self.user
        resp = createTemplate(request)

        self.assertEqual(resp.status_code, 302)

        template = ContestTemplate.objects.latest('id')
        self.assertEqual(template.title, "Contest test 1")


class CreateContestViewTest(TestCase):

    fixtures = ['users.json', 'teams.json', 'contests.json']

    def setUp(self):
        # Every test needs access to the request factory and authorized user
        self.factory = RequestFactory()
        self.client.login(username='testuser', password='password')
        self.user = auth.get_user(self.client)

    # Austin
    def test_not_post(self):
        request = reverse("contests:create_contest")
        resp = self.client.get(request, follow=True)

        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_create_contest(self):

        data = {
            "title": "Contest test creation", "creator": 1, "languages": "['1', '2', '3']",
            "contest_length": "02:00", "time_penalty": "20",
            "autojudge_enabled": "0", "autojudge_review": "",
            "problem_description": "hi.txt",
            "contest_admins": [2], "contest_participants": [1, 2],
            "submit": "create_contest",
            "form-TOTAL_FORMS": 1, "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 0, "form-MAX_NUM_FORMS": 1000
        }
        files = {
            "problem_description": SimpleUploadedFile("hi.txt", b"test problem desc")
        }

        request = self.factory.post(reverse("contests:create_contest"), data)
        request.user = self.user
        request.FILES.update(files)

        resp = createContest(request)
        self.assertEqual(resp.status_code, 302)

        contest = Contest.objects.latest('date_created')
        self.assertEqual(contest.title, "Contest test creation")
        participants = Participant.objects.filter(contest_id=contest.id)
        self.assertEqual(participants.count(), 0) # participant is updated after a team accept the inviation,
                                                  # thus should be 0 when contest just created


class EditContestViewTest(TestCase):

    fixtures = ['users.json', 'teams.json', 'contests.json', 'problems.json']

    # Austin
    def test_user_denied(self):
        self.client.login(username='admin', password='admin')
        assert self.user.is_authenticated()
        request = reverse("contests:edit_contest", kwargs={'contest_id': 22})
        resp = self.client.get(request)

        self.assertEqual(resp.status_code, 403)

    def setUp(self):
        # Every test needs access to the request factory and authorized user
        self.factory = RequestFactory()
        self.client.login(username='testuser', password='password')
        self.user = auth.get_user(self.client)

    # Austin
    def test_user_allowed(self):
        assert self.user.is_authenticated()
        request = reverse("contests:edit_contest", kwargs={'contest_id': 22})
        resp = self.client.get(request)

        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_not_post(self):
        request = reverse("contests:edit_contest", kwargs={'contest_id': 22})
        resp = self.client.get(request, follow=True)

        self.assertEqual(resp.status_code, 200)

    # Austin
    def test_contest_not_found(self):
        request = reverse("contests:edit_contest", kwargs={'contest_id': 9999})
        resp = self.client.get(request)

        self.assertEqual(resp.status_code, 404)

    # Austin
    def test_update_contest(self):
        contest_id = 22

        contest = Contest.objects.get(pk=contest_id)
        self.assertEqual(contest.title, "test contest")

        data = {
            "title": "edited test contest",
            "creator": "testuser",
            "languages": "['1', '2', '3']",
            "contest_length": "02:00",
            "time_penalty": "20",
            "autojudge_enabled": "0",
            "autojudge_review": "",
            "problem_description": "hi.txt",
            "contest_admins": [2],
            "contest_participants": [1, 2],
            "submit": "update_contest"
        }
        files = {
            "problem_description": SimpleUploadedFile("hi.txt", b"test problem desc")
        }

        request = self.factory.post(reverse("contests:edit_contest", kwargs={'contest_id': contest_id}), data)
        request.user = self.user
        request.FILES.update(files)

        resp = editContest(request, contest_id)
        self.assertEqual(resp.status_code, 200)

        contest.refresh_from_db()
        self.assertEqual(contest.title, "edited test contest")

    # Austin
    def test_update_problem(self):
        contest_id = 22
        problem_id = 1

        problem = Problem.objects.get(pk=problem_id)

        data = {
            "problem_id": problem_id,
            "solution": "uploads/test1.txt",
            "input_description": "edited problem 1 input",
            "output_description": "problem 1 output",
            "sample_input": "",
            "sample_output": "edited 1 2 3",
            "contest": contest_id,
            "timeout": 5,
            "submit": "update_problem"
        }
        files = {
            "solution": SimpleUploadedFile("sol.txt", b"test solution"),
            "sample_input": SimpleUploadedFile("input.txt", b"edited a b c"),
            "sample_output": SimpleUploadedFile("output.txt", b"edited 1 2 3")
        }

        request = self.factory.post(reverse("contests:edit_contest", kwargs={'contest_id': contest_id}), data)
        request.user = self.user
        request.FILES.update(files)

        resp = editContest(request, contest_id)
        self.assertEqual(resp.status_code, 200)

        problem.refresh_from_db()
        self.assertEqual(problem.input_description, "edited problem 1 input")
        self.assertEqual(problem.sample_input.read(), b"edited a b c")
        self.assertEqual(problem.sample_output.read(), b"edited 1 2 3")

    # Austin
    def test_delete_problem(self):
        contest_id = 22
        problem_id = 1

        self.assertTrue(Problem.objects.filter(pk=problem_id).exists())
        self.assertTrue(Problem.objects.filter(contest_id=contest_id).count(), 2)

        data = {
            "problem_id": problem_id,
            "submit": "delete_problem"
        }

        request = self.factory.post(reverse("contests:edit_contest", kwargs={'contest_id': contest_id}), data)
        request.user = self.user

        resp = editContest(request, contest_id)
        self.assertEqual(resp.status_code, 200)

        self.assertFalse(Problem.objects.filter(pk=problem_id).exists())
        self.assertTrue(Problem.objects.filter(contest_id=contest_id).count(), 1)

    # Austin
    def test_save_new_problem(self):
        contest_id = 22

        self.assertTrue(Problem.objects.filter(contest_id=contest_id).count(), 2)

        data = {
            "solution": "sol3.txt",
            "input_description": "problem 3 input desc",
            "output_description": "problem 3 output desc",
            "sample_input": "input3.txt",
            "sample_output": "output3.txt",
            "contest": contest_id,
            "submit": "save_new_problem"
        }
        files = {
            "solution": SimpleUploadedFile("sol3.txt", b"problem 3 solution"),
            "sample_input": SimpleUploadedFile("input3.txt", b"problem 3 sample input"),
            "sample_output": SimpleUploadedFile("output3.txt", b"problem 3 sample output")
        }

        request = self.factory.post(reverse("contests:edit_contest", kwargs={'contest_id': contest_id}), data)
        request.user = self.user
        request.FILES.update(files)

        resp = editContest(request, contest_id)
        self.assertEqual(resp.status_code, 200)

        self.assertTrue(Problem.objects.filter(contest_id=contest_id).count(), 3)
        problem = Problem.objects.latest('id')
        self.assertEqual(problem.input_description, "problem 3 input desc")
        self.assertEqual(problem.sample_output.read(), b"problem 3 sample output")


class TemplateTagTest(TestCase):

    # Vivian
    def test_tag_index(self):
        template = "{{ my_list|index:2 }}"
        context = {"my_list": [1,2,3]}
        output = u"2"
        t = Template('{% load contest_extras %}'+template)
        c = Context(context)
        self.assertEqual(t.render(c), output)

    # Vivian
    def test_tag_printfile(self):
        template = "{{ my_file|print_file_content }}"
        context = {"my_file": SimpleUploadedFile("foo.txt", b"foo"),}
        output = u"foo"
        t = Template('{% load contest_extras %}'+template)
        c = Context(context)
        self.assertEqual(t.render(c), output)

    # Vivian
    def test_tag_printfile_nullfile(self):
        template = "{{ my_file|print_file_content }}"
        context = {"my_file": None}
        output = u""
        t = Template('{% load contest_extras %}'+template)
        c = Context(context)
        self.assertEqual(t.render(c), output)

    # Vivian
    def test_tag_printfile_closedfile(self):
        template = "{{ my_file|print_file_content }}"
        my_file = SimpleUploadedFile("foo.txt", b"foo")
        my_file.close()
        context = {"my_file": my_file }
        output = u""
        t = Template('{% load contest_extras %}'+template)
        c = Context(context)
        self.assertEqual(t.render(c), output)
