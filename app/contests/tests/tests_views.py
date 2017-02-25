from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
from contests.forms import ReturnJudgeResultForm, CreateContestForm
from contests.models import Team, Participant, Contest, Problem, Submission, ContestTemplate


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

    # # Vivian
    # TODO: this need to be refactored after the contest participant/admin field is changed
    # def test_view_contest_participant(self):
    #     self.client.login(username='participant1', password='password')
    #     user = auth.get_user(self.client)
    #     assert user.is_authenticated()
    #
    #     url = reverse("contests:contest", kwargs={'contest_id': 7})
    #     resp = self.client.get(url)
    #     self.assertEqual(resp.status_code, 200)

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

    #Austin
    def test_load_valid_template(self):
        self.client.login(username='testuser', password='password')

        data = {"selected_template": 1, "submit": "load_template"}
        resp = self.client.post(reverse('contests:create'), data=data)
        self.assertEqual(resp.status_code, 200)

    #Austin
    def test_redirect_create_template_page(self):
        self.client.login(username='testuser', password='password')

        resp = self.client.get(reverse('contests:create_template'))
        self.assertEqual(resp.status_code, 200)

    #Austin
    def test_create_template(self):
        self.client.login(username='testuser', password='password')

        data = {
            "title": "Contest test 1", "languages": "java, python",
            "contest_length": "02:00", "time_penalty": "20",
            "autojudge_enabled": "0", "autojudge_review": "",
            "contest_participants": ""
        }
        resp = self.client.post(reverse('contests:create_template'), follow=True, data=data)
        self.assertRedirects(resp, reverse('contests:index'), target_status_code=200)

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