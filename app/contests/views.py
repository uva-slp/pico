from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect

from teams.forms import TeamForm, TeamSelectForm

from organizations.forms import OrganizationForm, OrganizationJoinForm, OrganizationLeaveForm
from .models import Problem, Contest
from .forms import CreateContestForm, CreateProblem, UploadCodeForm, ReturnJudgeResultForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.urls import reverse
from .lib import diff as _diff
from .lib import execution as exe
from .models import Contest, Problem, ContestTemplate
from teams.models import Team
from .forms import CreateContestTemplateForm
from .models import Participant, Submission, Notification
from users.models import User
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import Http404
import os

from django.forms.formsets import formset_factory

def index(request):
    all_active_contests = Contest.objects.active()
    my_active_contests = []
    for contest in all_active_contests:
        if isCreator(contest, request.user) or isJudge(contest, request.user) or isParticipant(contest, request.user):
            my_active_contests.append(contest)

    all_pending_contests = Contest.objects.pending()
    my_pending_contests = []
    for contest in all_pending_contests:
        if isCreator(contest, request.user) or isJudge(contest, request.user) or isParticipant(contest, request.user):
            my_pending_contests.append(contest)

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
            'pending_contests': my_pending_contests,
            'past_contests': my_past_contests,
        }
    )

def choose_problem(request):
    all_problems = Problem.objects.all()
    return render(request, 'contests/choose_problem.html', {'problems': all_problems})


def upload_code(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    form = UploadCodeForm(initial = {'problem': problem})
    return render(request, 'contests/upload_page.html', {'form': form, 'problem': problem})


def diff(request, problem_id):
        form = UploadCodeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            output = exe.execute_code(request.FILES['code_file'])
            retcode = output[0]
            if retcode != 0:
                    error = output[1]
                    return render(request, 'contests/error.html', {'error_message' : error})
            else:
                    fromlines = output[1].split("\n")
                    tolines = ['Hello World from C++!']
                    html, numChanges = _diff.HtmlFormatter(fromlines, tolines, False).asTable()
                    return render(request, 'contests/diff.html', {'diff_table': html, 'numChanges': numChanges})
        else:
                return render(request, 'contests/error.html', {'error_message' : "Invalid form."})


def create(request):

        QAFormSet = formset_factory(CreateProblem)
        templates = None
    
        if request.method == 'POST':
                if request.POST['submit'] == "load_template":
                        selected_template = request.POST['selected_template']

                        if selected_template:
                                template = ContestTemplate.objects.get(pk=selected_template)
                                form = CreateContestForm(initial={'title': template.title, 'languages': template.languages,
                                                                                                  'contest_length': template.contest_length,
                                                                                                  'time_penalty': template.time_penalty,
                                                                                                  'autojudge_enabled': template.autojudge_enabled,
                                                                                                  'autojudge_review': template.autojudge_review,
                                                                                                  'contest_admins': template.contest_admins,
                                                                                                  'contest_participants': template.contest_participants
                                                                                                  })

                                template_user = request.user
                                templates = ContestTemplate.objects.filter(creator=template_user)
                                QAFormSet = formset_factory(CreateProblem)
                                qa_formset = QAFormSet()

                                return render(request, 'contests/create_contest.html',
                                                          {'templates': templates, 'form': form, 'qa_formset': qa_formset})

                        else:
                                # template does not exist or no template was selected
                                create()
                if request.POST['submit'] == "create_contest":
                        #grab information from form
                        form = CreateContestForm(request.POST, request.FILES)
                        #qa_formset = CreateProblem(request.POST, request.FILES)

                        qa_formset = QAFormSet(request.POST, request.FILES)
                        if form.is_valid() and qa_formset.is_valid():

                                problem_desc = Contest(problem_description=request.FILES['problem_description'], date_created=datetime.now(timezone.utc))

                                contest = form.save()
                                contest.creator = request.user
                                contest.save()

                                contest_id = contest.id

                                contest_participants = form.cleaned_data.get('contest_participants')
                                contest_participants = contest_participants.split()
                                print(contest_participants)

                                for participant in contest_participants : # Loop through the given participants when a user creates a contest and create participant objects for each
                                        team = Team.objects.filter(name=participant).get()
                                        print(team)
                                        pt = Participant(contest=contest, team=team)
                                        print(pt)
                                        pt.save()

                                problemcount = 0

                                for qa_form in qa_formset:
                                        problemcount += 1
                                        solution = qa_form.cleaned_data.get('solution')
                                        program_input = qa_form.cleaned_data.get('program_input')
                                        input_desc = qa_form.cleaned_data.get('input_description')
                                        output_desc = qa_form.cleaned_data.get('output_description')
                                        sample_input = qa_form.cleaned_data.get('sample_input')
                                        sample_output = qa_form.cleaned_data.get('sample_output')
                                        contest = qa_form.cleaned_data.get('title')

                                        p = Problem(
                                                number = problemcount, solution=solution, program_input = program_input, input_description=input_desc,
                                                output_description=output_desc, sample_input=sample_input,
                                                sample_output=sample_output, contest_id=contest_id)

                                        p.save()

                                        # Loop through participants text box and create participant objects for a team on each line w/ contest

                                return redirect(reverse('home'))
        else:
                template_user = request.user
                templates = ContestTemplate.objects.filter(creator=template_user)
                form = CreateContestForm()
                QAFormSet = formset_factory(CreateProblem)
                qa_formset = QAFormSet()
        return render(request, 'contests/create_contest.html', {'templates': templates, 'form': form, 'qa_formset': qa_formset})


def create_template(request):
        if request.method == 'POST':
                form = CreateContestTemplateForm(request.POST)

                if form.is_valid():
                        contest_template = form.save()
                        contest_template.creator = request.user
                        contest_template.save()

                        return redirect(reverse('home'))
        else:
                form = CreateContestTemplateForm()
        return render(request, 'contests/create_template.html', {'form': form})


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
    # TODO need to be changed after we have actual admin field
    contest_judges = contest_data.contest_admins
    contest_judges = contest_judges.split()
    for judge in contest_judges:
        if user.username == judge:
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
            print("HERE")
            form = UploadCodeForm(request.POST, request.FILES)
            if form.is_valid():
                sub = form.save(commit=False)
                sub.original_filename = request.FILES['code_file'].name
                sub.team = current_team
                sub.save()

    problems = contest_data.problem_set.all()
    #Handle multiple forms on the same page
    UploadCodeFormSet = formset_factory(UploadCodeForm, extra = len(problems))
    problem_form_pairs = []
    for problem in problems:
        form = UploadCodeForm(initial={'problem' : problem})
        problem_form_pairs.append((problem, form))

    contest_participants = contest_data.participant_set.all()
    contest_teams = []
    for participant in contest_participants:
        contest_teams.append(participant.team)

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


    return render( request, 'contests/contest.html', {'contest_data': contest_data, 'contest_problems': problems,
                                                      'is_judge': is_judge, 'is_participant': is_participant,
                                                      'contest_teams': contest_teams, 'submission_attempts': submission_attempts,
                                                      'submission_status': status, 'color_states': color_states,
                                                      'problem_form_pairs' : problem_form_pairs })


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
        {'contest_data': contest_data, 'new_submissions': new_submissions, 'judged_submissions': judged_submissions}
    )


@login_required
def displayMySubmissions(request, contest_id, team_id):
    contest_data = Contest.objects.get(id=contest_id)
    team = Team.objects.get(id=team_id)

    is_judge = isJudge(contest_data, request.user)
    if not is_judge and request.user not in team.members.all():
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
                        output = exe.execute_code(getattr(current_submission, 'code_file'), getattr(current_submission, 'original_filename'), getattr(getattr(current_submission, 'problem'), 'program_input'))
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


def scoreboard(request, contest_id):

    scoreboard_contest = Contest.objects.get(id=contest_id) # Get contest ID from URL
    problems = Problem.objects.all()
    problems = problems.filter(contest=scoreboard_contest) # Filter problems to look at by contest
    problem_count = 0
    for problem in problems :
        problem_count += 1
        print("problem:")
        print(problem.number)

    participants_string = scoreboard_contest.contest_participants
    participants_string = participants_string.split()

    problem_count_array = []
    for i in range(1, problem_count+1):
        problem_count_array.append(i)

    contest_title = scoreboard_contest.title

    problems_status_array = {}
    problem_score_array = {}
    problem_attempts_array = {}

    #for problem in problems:
    #    problems_status_array[problem] = [2]


    for teamname in participants_string:
        try:
            tempteam = Team.objects.get(name=teamname)
        except:
            raise Http404("Team in scoreboard no longer exists")
        # array with [teamname][121001] based on submission>?

        problem_score_array[teamname] = 0
        problem_attempts_array[teamname] = 0

        templist = []
        # need to iterate through submissions for each team and only edit html per team

        for problem in problems: # Iterate through problems and check submissions for right/wrong answer
            #newteam = getTeam(scoreboard_contest, request.user)


            print("problem: ")
            print(problem)

            tempsubmission = Submission.objects.filter(team = tempteam, problem=problem).last()

            print("tempsubmission: ")
            print(tempsubmission)

            #filter submission by problem/team
            if(tempsubmission is None): # no submission given for this problem
                templist.append("3")
                problems_status_array[teamname] = templist
                break
            elif(tempsubmission.result == 'YES') : # Correct answer
                templist.append("1")
                #tempscore += 1
                problems_status_array[teamname] = templist
                problem_score_array[teamname] += 1
            elif(tempsubmission.result == 'WRONG' or tempsubmission.result == 'OFE' or tempsubmission.result == 'IE' or tempsubmission.result == 'EO' or tempsubmission.result == 'CE' or tempsubmission.result == 'RTE' or tempsubmission.result == 'TLE' or tempsubmission.result == 'OTHER'): # Red
                templist.append("0")
                problems_status_array[teamname] = templist
            else:
                templist.append("2")
                problems_status_array[teamname] = templist # Otherwise the submission is pending

            print("tempstring")
            print(templist)
            print("problems status array: ")
            print(problems_status_array)
            #print(problem_score_array)

    


    return render(request, 'contests/scoreboard.html', {'teams' : participants_string, 'problem_count' : problem_count_array,
        'problems' : problems, 'contest_title' : contest_title, 'problem_status_array' : problems_status_array, 'problem_score_array' : problem_score_array})


def show_notification(request):
    l = []

    all_notifications = Notification.objects.all()
    for noti in all_notifications:
        submission = noti.submission
        team = submission.team
        if request.user in team.members.all():
            # data needed for showing notification
            # contest title, problem, run id, and result
            current_data = (submission.problem.contest.title, submission.problem.number,
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

def stats(request):
    contest_participation = Participant.objects.all()
    return render(request, 'contests/stats.html', {'contest_participation' : contest_participation})