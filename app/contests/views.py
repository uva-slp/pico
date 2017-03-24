from django.http import HttpResponse, HttpResponseForbidden, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from teams.forms import TeamForm, TeamSelectForm
from .forms import CreateContestForm, CreateProblem, UploadCodeForm, ReturnJudgeResultForm, CreateContestTemplateForm, AdminSearchForm, ParticipantSearchForm
from dal import autocomplete
from users.forms import UserSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory, inlineformset_factory
from django.urls import reverse
from .lib import diff as _diff
from .lib import execution as exe
from .models import Contest, Problem, ContestTemplate
from teams.models import Team
from .models import Participant, Submission, Notification
from users.models import User
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import Http404
from django.template.loader import render_to_string
import os
from subprocess import Popen


def index(request):
    all_active_contests = Contest.objects.active()
    my_active_contests = []
    for contest in all_active_contests:
        if isCreator(contest, request.user) or isJudge(contest, request.user) or isParticipant(contest, request.user):
            my_active_contests.append(contest)

    all_unstarted_contests = Contest.objects.unstarted()
    my_unstarted_contests = []
    for contest in all_unstarted_contests:
        if isCreator(contest, request.user) or isJudge(contest, request.user) or isParticipant(contest, request.user):
            my_unstarted_contests.append(contest)

    all_past_contests = Contest.objects.past()
    my_past_contests = []
    for contest in all_past_contests:
        if isCreator(contest, request.user) or isJudge(contest, request.user) or isParticipant(contest, request.user):
            my_past_contests.append(contest)

    return render(
        request,
        'contests/index.html',
        {
            'active_contests': my_active_contests,
            'unstarted_contests': my_unstarted_contests,
            'past_contests': my_past_contests,
        }
    )


@login_required
def create(request):

    template_user = request.user
    templates = ContestTemplate.objects.filter(creator=template_user)

    QAFormSet = formset_factory(CreateProblem)
    qa_formset = QAFormSet()

    form = CreateContestForm()
    admin_search_form = AdminSearchForm()
    participant_search_form = ParticipantSearchForm()

    if request.method == 'POST':
        if request.POST['submit'] == "load_template":
            selected_template = request.POST['selected_template']

            if ContestTemplate.objects.filter(pk=selected_template).exists():
                template = ContestTemplate.objects.get(pk=selected_template)
                form = CreateContestForm(initial={
                        'title': template.title, 'languages': template.languages,
                        'contest_length': template.contest_length, 'time_penalty': template.time_penalty,
                        'autojudge_enabled': template.autojudge_enabled, 'autojudge_review': template.autojudge_review,
                        'contest_admins': template.contest_admins.all(), 'contest_participants': template.contest_participants.all()
                    }
                )

                admin_search_form = AdminSearchForm(
                    initial={'contest_admins': template.contest_admins.all()})
                participant_search_form = ParticipantSearchForm(
                    initial={'contest_participants': template.contest_participants.all()})

                data = {
                    'templates': templates,
                    'form': form,
                    'qa_formset': qa_formset,
                    'admin_search_form': admin_search_form,
                    'participant_search_form': participant_search_form
                }

                return render(request, 'contests/create_contest.html', data)

        if request.POST['submit'] == "create_contest":
            #grab information from form
            form = CreateContestForm(request.POST, request.FILES)
            qa_formset = QAFormSet(request.POST, request.FILES)

            if form.is_valid() and qa_formset.is_valid():

                problem_desc = Contest(problem_description=request.FILES['problem_description'], date_created=datetime.now(timezone.utc))

                contest = form.save()
                contest.creator = request.user
                contest.save()

                contest_id = contest.id

                contest_participants = form.cleaned_data.get('contest_participants')

                for participant in contest_participants : # Loop through the given participants when a user creates a contest and create participant objects for each
                    team = Team.objects.filter(name=participant).get()
                    pt = Participant(contest=contest, team=team)
                    pt.save()

                for qa_form in qa_formset:
                    qa_form = qa_form.cleaned_data
                    create_new_problem(request, qa_form, contest_id)

                    # Loop through participants text box and create participant objects for a team on each line w/ contest

                return redirect(reverse('home'))

    data = {
        'templates': templates,
        'form': form,
        'qa_formset': qa_formset,
        'admin_search_form': admin_search_form,
        'participant_search_form': participant_search_form
    }

    return render(request, 'contests/create_contest.html', data)


@login_required
def create_new_problem(request, form, contest_id):
    solution = form.get('solution')
    program_input = form.get('program_input')
    input_desc = form.get('input_description')
    output_desc = form.get('output_description')
    sample_input = form.get('sample_input')
    sample_output = form.get('sample_output')

    p = Problem(
        solution=solution, program_input=program_input, input_description=input_desc,
        output_description=output_desc, sample_input=sample_input,
        sample_output=sample_output, contest_id=contest_id
    )

    p.save()


@login_required
def edit(request, contest_id):

    contest = get_object_or_404(Contest, pk=contest_id)
    if contest.creator != request.user:
        return HttpResponseForbidden()

    form = CreateContestForm(None, None, instance=contest)

    admin_search_form = AdminSearchForm(initial={'contest_admins': contest.contest_admins.all()})
    participant_search_form = ParticipantSearchForm(initial={'contest_participants': contest.contest_participants.all()})

    problem_form = CreateProblem()

    problems = contest.problem_set.all()
    problems_set = []
    for problem in problems:
        problems_set.append((problem.id, CreateProblem(instance=problem)))

    if request.method == 'POST':
        if request.POST['submit'] == "update_contest":

            form = CreateContestForm(request.POST, request.FILES, instance=contest)

            if form.is_valid():
                problem_desc = Contest(problem_description=request.FILES.get('problem_description', False),
                                       date_created=datetime.now(timezone.utc))
                form.save()

                contest_participants = form.cleaned_data.get('contest_participants')

                for participant in contest_participants:  # Loop through the given participants when a user creates a contest and create participant objects for each
                    if participant not in Contest.objects.values_list('contest_participants', flat=True).filter(pk=contest_id):
                        team = Team.objects.filter(name=participant).get()
                        pt = Participant(contest=contest, team=team)
                        pt.save()

                request.method = None
                request.POST = None
                return edit(request, contest_id)

        if request.POST['submit'] == "update_problem":
            problem_id = request.POST['problem_id']
            problem = Problem.objects.get(pk=problem_id)
            problem_form = CreateProblem(request.POST or None, request.FILES or None, instance=problem)
            if problem_form.is_valid():
                problem_form.id = problem_id
                problem_form.save()

            request.method = None
            request.POST = None
            return edit(request, contest_id)

        if request.POST['submit'] == "delete_problem":
            problem_id = request.POST['problem_id']
            Problem.objects.get(pk=problem_id).delete()

            request.method = None
            request.POST = None
            return edit(request, contest_id)

        if request.POST['submit'] == "save_new_problem":
            problem_form = CreateProblem(request.POST, request.FILES)
            if problem_form.is_valid():
                problem_form = problem_form.cleaned_data
                create_new_problem(request, problem_form, contest_id)

            request.method = None
            request.POST = None
            return edit(request, contest_id)

    data = {
        'form': form,
        'admin_search_form': admin_search_form,
        'participant_search_form': participant_search_form,
        'problem_form': problem_form,
        'problems_set': problems_set,
        'contest_id': contest_id
    }

    return render(request, 'contests/edit_contest.html', data)


@login_required
def create_template(request):

    form = CreateContestTemplateForm()
    admin_search_form = AdminSearchForm()
    participant_search_form = ParticipantSearchForm()

    if request.method == 'POST':
        form = CreateContestTemplateForm(request.POST)

        if form.is_valid():
            contest_template = form.save()
            contest_template.creator = request.user
            contest_template.save()

            return redirect(reverse('home'))

    data = {
        'form': form,
        'admin_search_form': admin_search_form,
        'participant_search_form': participant_search_form
     }

    return render(request, 'contests/create_template.html', data)


# Helper method for getting user's team participated in a contest
def getTeam(contest_data, user):
    user = User.objects.get(id=user.id)
    contest_data = Contest.objects.get(id=contest_data.id)
    contest_participants = contest_data.participant_set.all()
    for participant in contest_participants:
            team = participant.team
            if user in team.members.all():
                    return team
    return None


# Helper method for checking if user is judge of the contest
def isJudge(contest_data, user):
    contest_judges = contest_data.contest_admins.all()
    for judge in contest_judges:
        if user == judge:
            return True
    return False


# Helper method for checking if user is creator of the contest
def isCreator(contest_data, user):
    if user == contest_data.creator:
        return True
    return False


# Helper method for checking if user is participant in the contest
def isParticipant(contest_data, user):
	current_team = getTeam(contest_data, user)
	if current_team is None:
		return False
	else:
		return True


@login_required
def displayContest(request, contest_id):

    # Check if request user has permission to view the page
    contest_data = Contest.objects.get(id=contest_id)
    is_judge = isJudge(contest_data, request.user)
    is_participant = isParticipant(contest_data, request.user)
    is_creator = isCreator(contest_data, request.user)
    current_team = getTeam(contest_data, request.user)

    if not is_judge and not is_participant and not is_creator and not request.user.is_superuser:
        return redirect(reverse('home'))

    # Activate Contest or save the submission
    if request.method == 'POST':
        if 'submit' in request.POST and request.POST['submit'] == "activate_contest":
            time = datetime.now()
            contest = Contest.objects.get(id=contest_id)
            contest.contest_start = time
            contest.save()
            return redirect(reverse('home'))
        else:
            form = UploadCodeForm(request.POST, request.FILES)
            if form.is_valid():
                sub = form.save(commit=False)
                sub.original_filename = request.FILES['code_file'].name
                sub.team = current_team
                sub.save()

    problems = contest_data.problem_set.all()
    #Handle multiple forms on the same page
    UploadCodeFormSet = formset_factory(UploadCodeForm, extra=len(problems))
    problem_form_pairs = []
    for problem in problems:
        form = UploadCodeForm(initial={'problem': problem})
        problem_form_pairs.append((problem, form))

    contest_participants = contest_data.participant_set.all()

    current_team = getTeam(contest_data, request.user)
    submission_attempts = []
    status = []
    color_states = []
    if current_team is not None:
        for p in problems:
            p_submissions = p.submission_set.filter(team__pk=current_team.id)
            # number of attempts
            current_attempts = len(p_submissions)
            submission_attempts.append(current_attempts)
            # status -- ignore the rest
            current_status = "-"
            current_color = "default"
            if current_attempts is not 0:
                got_yes = False
                for s in p_submissions:
                    if s.state == 'YES':
                        got_yes = True
                        break
                if got_yes:
                    current_status = "Yes"
                    current_color = "success"
                else:
                    submissions = list(p_submissions)
                    submissions.sort(key=lambda x: x.timestamp)
                    latest_submission = submissions[-1]
                    if latest_submission.state == 'NEW':
                        current_color = "warning"
                        current_status = "New"
                    elif latest_submission.state == 'NO':
                        current_color = "danger"
                        current_status = "No - " + latest_submission.get_result_display()
            status.append(current_status)
            color_states.append(current_color)

    data = {
        'contest_data': contest_data, 'contest_problems': problems,
        'is_judge': is_judge, 'is_participant': is_participant, 'is_creator': is_creator,
        'current_team': current_team, 'submission_attempts': submission_attempts,
        'submission_status': status, 'color_states': color_states,
        'problem_form_pairs': problem_form_pairs
    }

    return render(request, 'contests/contest.html', data)


@login_required()
def displayProblemDescription(request, contest_id):
    contest_data = Contest.objects.get(id=contest_id)
    path = contest_data.problem_description.path
    with open(path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=%s.pdf' %contest_data.problem_description.name
        return response

@login_required
def displayAllSubmissions(request, contest_id):
    contest_data = Contest.objects.get(id=contest_id)

    is_judge = isJudge(contest_data, request.user)
    if not is_judge:
        return redirect(reverse('home'))

    problems = contest_data.problem_set.all()
    new_submissions = []
    judged_submissions = []
    for p in problems:
        submissions = list(p.submission_set.all())
        for sub in submissions:
            if sub.state == 'NEW':
                new_submissions.append(sub)
            else:
                judged_submissions.append(sub)
    new_submissions.sort(key=lambda x: x.timestamp)
    judged_submissions.sort(key=lambda x: x.timestamp)

    return render(
        request,
        'contests/all_submissions.html',
        {'contest_data': contest_data, 'new_submissions': new_submissions, 'judged_submissions': judged_submissions, 'is_judge': is_judge}
    )


@login_required
def displayMySubmissions(request, contest_id, team_id):
    contest_data = Contest.objects.get(id=contest_id)
    team = Team.objects.get(id=team_id)

    is_judge = isJudge(contest_data, request.user)
    if not is_judge and request.user not in team.members.all() and not request.user.is_superuser:
        return redirect(reverse('home'))

    problems = contest_data.problem_set.all()
    submissions = []
    for p in problems:
        submissions += list(p.submission_set.filter(team__pk=team_id))
    submissions.sort(key=lambda x: x.timestamp)

    return render(
        request,
        'contests/user_submissions.html',
        {'contest_data': contest_data, 'team': team, 'contest_submissions': submissions}
    )


@login_required
def displayJudge(request, contest_id, run_id):
        contest_data = Contest.objects.get(id=contest_id)
        is_judge = isJudge(contest_data, request.user)
        if not is_judge:
                return redirect(reverse('home'))
        
        problems = contest_data.problem_set.all()
        for p in problems:
                if p.submission_set.filter(run_id=run_id).exists():
                        current_submission = p.submission_set.get(run_id=run_id)
                        if request.method == 'POST':
                                form = ReturnJudgeResultForm(request.POST, instance=current_submission)
                                if form.is_valid():
                                        form.save()
                                        # create a new notification
                                        notification = Notification(submission=current_submission)
                                        notification.save()
                                        return redirect(reverse('contests:contest_judge_submissions',
                                                        kwargs={'contest_id': contest_id}))
                                else:
                                        messages.error(request, "Error")
                        else:
                                form = ReturnJudgeResultForm(instance=current_submission)
                        allowed_languages = getattr(contest_data, 'languages')
                        output = exe.execute_code(Popen, getattr(current_submission, 'code_file'), getattr(current_submission, 'original_filename'), getattr(getattr(current_submission, 'problem'), 'program_input'), allowed_languages, getattr(getattr(current_submission, 'problem'), 'timeout'))
                        retcode = output[0]
                        fromlines = output[1].split("\n")
                        solution_file = getattr(getattr(current_submission, 'problem'), 'solution')
                        #Use the solution file if it exists. If not, use empty expected output.
                        tolines = []
                        if bool(solution_file) and os.path.isfile(solution_file.name):
                                tolines = solution_file.read().decode().split("\n")
                        html, numChanges = _diff.HtmlFormatter(fromlines, tolines, False).asTable()
                        return render(request, 'contests/judge.html', {'diff_table': html, 'numChanges': numChanges, 'contest_data': contest_data, 'is_judge': True, 'submission': current_submission, 'form': form})

        return render(
                request,
                'contests/judge.html',
                {'contest_data': contest_data, 'is_judge': False}
        )

def stats(request):
    if request.user.is_authenticated():
        participation = Participant.objects.filter(team__members__username=request.user.username).order_by('contest__date_created')
        contest_count = Participant.objects.filter(team__members__username=request.user.username).count()
        teams = Team.objects.filter(members__username=request.user.username).order_by('name')
        teams_count = teams.count()
        teammates_count = 0
        for t in teams:
            members = t.members.all()
            for m in members:
                if m.username != request.user.username:
                    teammates_count += 1
        return render(request, 'contests/stats.html', { 'participation' : participation,
                                                        'contest_count' : contest_count,
                                                        'teams' : teams,
                                                        'teams_count' : teams_count,
                                                        'teammates_count' : teammates_count})
    else:
        return render(request, 'contests/stats.html')


def scoreboard(request, contest_id):

    scoreboard_contest = Contest.objects.get(id=contest_id) # Get contest ID from URL
    problems = Problem.objects.all()
    problems = problems.filter(contest=scoreboard_contest) # Filter problems to look at by contest
    problem_number = 0
    for problem in problems:
        problem_number += 1

    participants = scoreboard_contest.participant_set.all()

    problem_count_array = []
    for i in range(1, problem_number+1):
        problem_count_array.append(i)

    contest_title = scoreboard_contest.title

    problems_status_array = {}
    problem_score_array = {}
    problem_attempts_array = {}

    for participant in participants:
        teamname = participant.team.name
        try:
            tempteam = Team.objects.get(name=teamname)
        except:
            raise Http404("Team in scoreboard no longer exists")

        problem_score_array[teamname] = 0
        problem_attempts_array[teamname] = 0
        templist = []

        for problem in problems: # Iterate through problems and check submissions for right/wrong answer
            tempsubmission = Submission.objects.filter(team = tempteam, problem = problem)
            for object in tempsubmission :
                problem_attempts_array[teamname] += 1


            tempsubmission = Submission.objects.filter(team = tempteam, problem=problem).last()

            #filter submission by problem/team
            if(tempsubmission is None): # no submission given for this problem
                templist.append("3")
                problems_status_array[teamname] = templist
                continue
            elif(tempsubmission.result == 'YES') : # Correct answer
                templist.append("1")
                problems_status_array[teamname] = templist
                problem_score_array[teamname] += 1
            elif(tempsubmission.result == 'WRONG' or tempsubmission.result == 'OFE' or tempsubmission.result == 'IE' or tempsubmission.result == 'EO' or tempsubmission.result == 'CE' or tempsubmission.result == 'RTE' or tempsubmission.result == 'TLE' or tempsubmission.result == 'OTHER'): # Red
                templist.append("0")
                problems_status_array[teamname] = templist
            else:
                templist.append("2")
                problems_status_array[teamname] = templist # Otherwise the submission is pending

    data = {
        'problem_number' : problem_count_array,
        'contest_title' : contest_title, 'problem_status_array' : problems_status_array,
        'problem_score_array' : problem_score_array, 'contest_data':scoreboard_contest,
        'problem_attempts_array': problem_attempts_array
    }

    print("attempts")
    print(problem_attempts_array)


    return render(request, 'contests/scoreboard.html', data)


def show_notification(request):
    l = []

    all_notifications = Notification.objects.all()
    for noti in all_notifications:
        submission = noti.submission
        team = submission.team
        if request.user in team.members.all():
            # data needed for showing notification

            noti_problem = Problem.objects.get(pk=submission.problem_id)
            problems = Problem.objects.filter(contest_id=noti_problem.contest_id)
            problem_number = 0
            for problem in problems:
                problem_number += 1
                if problem.id == noti_problem.id:
                    break

            # contest title, problem number, run id, and result
            current_data = (submission.problem.contest.title, problem_number,
                            submission.run_id, submission.get_result_display(), noti.id)
            l.append(current_data)

    d = {'data': l}
    return JsonResponse(d)


def close_notification(request):
    modal_id = request.POST['id']
    print("modal id: " + modal_id)
    if Notification.objects.filter(id=modal_id).exists():
        current_notification = Notification.objects.get(id=modal_id)
        current_notification.delete()
    return HttpResponse('OK')

def refresh_scoreboard(request):
    contest_id = request.POST.get('contestId', "0")

    contest_data = None

    if contest_id != 0:
        contest_data = Contest.objects.get(id=contest_id)

    problems = contest_data.problem_set.all()

    problem_number = 0
    for problem in problems:
        problem_number += 1

    participants = contest_data.participant_set.all()

    problem_count_array = []
    for i in range(1, problem_number + 1):
        problem_count_array.append(i)

    problems_status_array = {}
    problem_score_array = {}
    problem_attempts_array = {}

    for participant in participants:
        teamname = participant.team.name

        tempteam = Team.objects.get(name=teamname)

        problem_score_array[teamname] = 0
        problem_attempts_array[teamname] = 0
        templist = []


        for p in problems:

            tempsubmission = Submission.objects.filter(team = tempteam, problem = problem)
            for object in tempsubmission :
                problem_attempts_array[teamname] += 1

            tempsubmission = Submission.objects.filter(team = tempteam, problem=p).last()

            #filter submission by problem/team
            if(tempsubmission is None): # no submission given for this problem
                templist.append("3")
                problems_status_array[teamname] = templist
                continue
            elif(tempsubmission.result == 'YES') : # Correct answer
                templist.append("1")
                problems_status_array[teamname] = templist
                problem_score_array[teamname] += 1
            elif(tempsubmission.result == 'WRONG' or tempsubmission.result == 'OFE' or tempsubmission.result == 'IE' or tempsubmission.result == 'EO' or tempsubmission.result == 'CE' or tempsubmission.result == 'RTE' or tempsubmission.result == 'TLE' or tempsubmission.result == 'OTHER'): # Red
                templist.append("0")
                problems_status_array[teamname] = templist
            else:
                templist.append("2")
                problems_status_array[teamname] = templist # Otherwise the submission is pending

    print("problem status")
    print(problems_status_array)
    print("problem attempts")
    print(problem_attempts_array)

    data = {
        'problem_number': problem_count_array,
        'problem_status_array' : problems_status_array,
        'problem_score_array' : problem_score_array,
        'problem_attempts_array' : problem_attempts_array
    }

    return render(request, 'contests/scoreboard_div.html', data)


def refresh_submission(request):
    contest_id = request.POST.get('contestId', "0")
    print("contest_id: " + contest_id)

    new_submissions = []
    judged_submissions = []
    contest_data = None

    if contest_id is not "0":
        contest_data = Contest.objects.get(id=contest_id)

        problems = contest_data.problem_set.all()
        for p in problems:
            submissions = list(p.submission_set.all())
            for sub in submissions:
                if sub.state == 'NEW':
                    new_submissions.append(sub)
                else:
                    judged_submissions.append(sub)
        new_submissions.sort(key=lambda x: x.timestamp)
        judged_submissions.sort(key=lambda x: x.timestamp)

    return render(request, 'contests/submission_div.html',
                  {'contest_data': contest_data, 'new_submissions': new_submissions, 'judged_submissions': judged_submissions})
