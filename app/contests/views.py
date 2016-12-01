from django.shortcuts import render, redirect

from teams.forms import TeamForm, TeamJoinForm, TeamLeaveForm
from organizations.forms import OrganizationForm, OrganizationJoinForm, OrganizationLeaveForm
from .forms import CreateContestForm, CreateProblem, CreateContestTemplateForm, UploadCodeForm, ReturnJudgeResultForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.urls import reverse
from .lib import diff as _diff
from .lib import execution as exe
from .models import Contest, Problem, ContestTemplate
from teams.models import Team
from .models import Participant, Submission
from users.models import User
from datetime import datetime
from django.utils import timezone


def home(request):
	return render(
		request,
		'contests/home.html',
		{
			'team_form': TeamForm(),
			'team_join_form': TeamJoinForm(),
			'team_leave_form': TeamLeaveForm(),
			'organization_form': OrganizationForm(),
			'organization_join_form': OrganizationJoinForm(),
			'organization_leave_form': OrganizationLeaveForm(),
			'contests_created': Contest.objects.all()
		}
	)


def choose_problem(request):
    all_problems = Problem.objects.all()
    return render(request, 'contests/choose_problem.html', {'problems': all_problems})


def upload_code(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    form = UploadCodeForm(initial = {'problem': problem})
    return render(request, 'contests/upload_page.html', {'form': form, 'problem': problem})


def diff(request, question_id):
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
                    return render(request, 'contests/diff.html', {'diff_table': html, 'numChanges': numChanges, 'question_id' : question_id})
        else:
            return render(request, 'contests/error.html', {'error_message' : "Invalid form."})


def create(request):

	QAFormSet = formset_factory(CreateProblem)

	if request.method == 'POST':
		#grab information from form
		form = CreateContestForm(request.POST, request.FILES)
		#qa_formset = CreateProblem(request.POST)

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
				input_desc = qa_form.cleaned_data.get('input_description')
				output_desc = qa_form.cleaned_data.get('output_description')
				sample_input = qa_form.cleaned_data.get('sample_input')
				sample_output = qa_form.cleaned_data.get('sample_output')
				contest = qa_form.cleaned_data.get('title')

				p = Problem(
					number = problemcount, solution=solution, input_description=input_desc,
					output_description=output_desc, sample_input=sample_input,
					sample_output=sample_output, contest_id=contest_id)

				p.save()

				# Loop through participants text box and create participant objects for a team on each line w/ contest

			return redirect(reverse('contests:home'))
			# return render(request, 'contests/home.html', {'form': form, 'qa_formset': qa_formset})
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

			return redirect(reverse('contests:home'))
	else:
		form = CreateContestTemplateForm()
	return render(request, 'contests/create_template.html', {'form': form})

def load_template(request):
	if request.method == 'POST':
		selected_template = request.POST['selected_template']

		if selected_template:
			template = ContestTemplate.objects.get(pk=selected_template)
			form = CreateContestForm(initial={'title': template.title, 'languages': template.languages,
				'contest_length': template.contest_length, 'time_penalty': template.time_penalty,
				'autojudge_enabled': template.autojudge_enabled, 'autojudge_review': template.autojudge_review,
				'contest_admins': template.contest_admins, 'contest_participants': template.contest_participants
				})

			template_user = request.user
			templates = ContestTemplate.objects.filter(creator=template_user)
			QAFormSet = formset_factory(CreateProblem)
			qa_formset = QAFormSet()

			return render(request, 'contests/create_contest.html', {'templates': templates, 'form': form, 'qa_formset': qa_formset})

		else:
			# template does not exist or no template was selected
			create()


# Helper method for getting user's team participated in a contest
def getTeam(contest_id, user_id):
	user = User.objects.get(id=user_id)
	contest_data = Contest.objects.get(id=contest_id)
	contest_participants = contest_data.participant_set.all()
	for participant in contest_participants:
		team = participant.team
		if user in team.members.all():
			return team
	return None


@login_required
def displayContest(request, contest_id):
	contest_data = Contest.objects.get(id=contest_id)


	problems = contest_data.problem_set.all()

	contest_participants = contest_data.participant_set.all()

	current_team = getTeam(contest_id, request.user.id)
	submission_attempts = []
	status = []
	color_states = []
	if current_team is not None:
		for p in problems:
			p_submissions = p.submission_set.filter(team__pk=current_team.id)
			# number of attempts
			current_attempts = len(p_submissions)
			submission_attempts.append(current_attempts)
			# status -- if have got it correct, ignore the rest
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
	else:
		for p in problems:
			submission_attempts.append(0)
			status.append("-")
			color_states.append("default")

	return render(
		request,
		'contests/contest.html',
		{'contest_data': contest_data, 'contest_problems': problems,
			'contest_teams': contest_participants, 'submission_attempts': submission_attempts,
		 	'submission_status': status, 'color_states': color_states, 'team': current_team
		 }
	)


@login_required
def displayAllSubmissions(request, contest_id):
	contest_data = Contest.objects.get(id=contest_id)
	problems = contest_data.problem_set.all()
	submissions = []
	if request.user == contest_data.creator:
		for p in problems:
			submissions += list(p.submission_set.all())
		submissions.sort(key=lambda x: x.timestamp)

	return render(
		request,
		'contests/all_submissions.html',
		{'contest_data': contest_data, 'contest_submissions': submissions}
	)


@login_required
def displayMySubmissions(request, contest_id, team_id):
	contest_data = Contest.objects.get(id=contest_id)
	team = Team.objects.get(id=team_id)
	problems = contest_data.problem_set.all()
	submissions = []
	if request.user == contest_data.creator or request.user in team.members.all():
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
	problems = contest_data.problem_set.all()
	if request.user == contest_data.creator:
		for p in problems:
			if p.submission_set.filter(run_id=run_id).exists():
				current_submission = p.submission_set.get(run_id=run_id)

				if request.method == 'POST':
					form = ReturnJudgeResultForm(request.POST, instance=current_submission)
					if form.is_valid():
						form.save()
						return redirect(reverse('contests:contest_judge_submissions',
							kwargs={'contest_id': contest_id}))
					else:
						messages.error(request, "Error")
				else:
					form = ReturnJudgeResultForm(instance=current_submission)
		return render(
			request,
			'contests/judge.html',
			{'contest_data': contest_data, 'submission': current_submission, 'form': form}
		)

	return render(
		request,
		'contests/judge.html',
		{'contest_data': contest_data}
	)


# Method for getting nearest datetime
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

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


    for teamname in participants_string:
        print(teamname)
        tempteam = Team.objects.get(name=teamname)
        for problem in problems:
            if(Submission.objects.get(team=tempteam, problem=problem)):
                submission = Submission.objects.get(team=tempteam, problem=problem)
                #if(submission.result == "YES"):
                print(submission)




    return render(request, 'contests/scoreboard.html',
				  {'teams' : participants_string, 'problem_count' : problem_count_array,
		'problems' : problems, 'contest_title' : contest_title, 'contest_data': mostrecentcontest})
