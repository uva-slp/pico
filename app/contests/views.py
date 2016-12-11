from django.shortcuts import render, redirect

from teams.forms import TeamForm, TeamJoinForm, TeamLeaveForm

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
from .models import Participant, Submission
from users.models import User
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import Http404

#To render multiple forms on a contest page (since there are multiple problems in a contest)
from django.forms.formsets import formset_factory

def home(request):
	time_arr = Contest.objects.values_list('contest_start', 'contest_length')
	end_time = []
	for start, length in time_arr:
		if start:
			new_minute = start.minute + length.minute
			new_hour = start.hour + length.hour
			new_datetime = start + relativedelta(hours=new_hour, minutes=new_minute)
			end_time.append(new_datetime)
		else:
			end_time.append(start)

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
			'contests_created': zip(Contest.objects.all(), end_time),
			'time_now': datetime.now(timezone.utc),
			'teams_joined': Team.objects.all()
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


# Helper method for checking if user is judge of the contest
def isJudge(contest_data, user):
	# TODO need to be changed after we have actual admin field
	contest_judges = contest_data.contest_admins
	contest_judges = contest_judges.split()
	for judge in contest_judges:
		if user.username == judge:
			return True
	return False


# Helper method for checking if user is participant in the contest
def isParticipant(contest_id, user_id):
	current_team = getTeam(contest_id, user_id)
	if current_team is None:
		return False
	else:
		return True

@login_required
def displayContest(request, contest_id):
	# Check if request user has permission to view the page
	contest_data = Contest.objects.get(id=contest_id)
	is_judge = isJudge(contest_data, request.user)
	is_participant = isParticipant(contest_id, request.user.id)

	if not is_judge and not is_participant:
		return redirect(reverse('contests:home'))

	# Activate Contest or save the submission
	if request.method == 'POST':
		if 'submit' in request.POST and request.POST['submit'] == "activate_contest":
			time = datetime.now()
			contest = Contest.objects.get(id=contest_id)
			contest.contest_start = time
			contest.save()
		else:
			print("HERE")
			form = UploadCodeForm(request.POST, request.FILES)
			if form.is_valid():
				sub = form.save(commit=False)
				sub.original_filename = request.FILES['code_file'].name
				sub.save()

	problems = contest_data.problem_set.all()
	#Handle multiple forms on the same page
	UploadCodeFormSet = formset_factory(UploadCodeForm, extra = len(problems))
	problem_form_pairs = []
	for problem in problems:
		form = UploadCodeForm(initial={'problem' : problem})
		problem_form_pairs.append((problem, form))
	is_judge = False
	# TODO: Right now this only checks contest creator. Need to update to all judges
	if request.user == contest_data.creator:
		is_judge = True

	contest_participants = contest_data.participant_set.all()
	contest_teams = []
	for participant in contest_participants:
		contest_teams.append(participant.team)

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

	return render( request, 'contests/contest.html', {'contest_data': contest_data, 'contest_problems': problems, 'is_judge': is_judge, 'contest_teams': contest_teams, 'submission_attempts': submission_attempts, 'submission_status': status, 'color_states': color_states, 'problem_form_pairs' : problem_form_pairs })


@login_required
def displayAllSubmissions(request, contest_id):
	contest_data = Contest.objects.get(id=contest_id)

	is_judge = isJudge(contest_data, request.user)
	if not is_judge:
		return redirect(reverse('contests:home'))

	problems = contest_data.problem_set.all()
	submissions = []
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

	is_judge = isJudge(contest_data, request.user)
	if not is_judge and request.user not in team.members.all():
		return redirect(reverse('contests:home'))

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
		return redirect(reverse('contests:home'))

	problems = contest_data.problem_set.all()
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
			output = exe.execute_code(getattr(current_submission, 'code_file'), getattr(current_submission, 'original_filename'))
			retcode = output[0]
			if retcode != 0:
				error = output[1]
				return render(request, 'contests/error.html', {'error_message' : error})
			else:
				fromlines = output[1].split("\n")
								#TODO make tolines the expected output
				# tolines = getattr(getattr(current_submission, 'problem'), 'output_description').split('\n')
				tolines = ("Hello world from C++!").split('\n')
				html, numChanges = _diff.HtmlFormatter(fromlines, tolines, False).asTable()
				return render(request, 'contests/judge.html', {'diff_table': html, 'numChanges': numChanges, 'contest_data': contest_data, 'is_judge': True,
					'submission': current_submission, 'form': form})
			return render(
				request,
				'contests/judge.html',
				{'contest_data': contest_data, 'is_judge': True,
					'submission': current_submission, 'form': form}
			)

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

        for problem in problems: # Iterate through problems and check submissions for right/wrong answer

            tempstring = ""

            # tempsubmission = Submission.objects.filter(team = tempteam, problem=problem)
            # for submissions in tempsubmission:
            #    problem_attempts_array[teamname] += 1

            test_submission_correct = Submission(team=tempteam, problem=problem, run_id=1, code_file="", timestamp="", state = 'YES', result='YES')
            test_submission_incorrect = Submission(team=tempteam, problem=problem, run_id=2, code_file="", timestamp="", state = 'NO', result='WRONG')
            test_submission_pending = Submission(team=tempteam, problem=problem, run_id=3, code_file="", timestamp="", state = 'NEW', result='')

            #filter submission by problem/team
            if(test_submission_pending.result == 'YES') : #correct answer, update scoreboard with green (0 for red, 1 for green, 2 for yellow?
                tempstring += "1"
                #tempscore += 1
                problems_status_array[teamname] = tempstring
                problem_score_array[teamname] += 1
            elif(test_submission_pending.result == 'WRONG'): # Red
                tempstring += "0"
                problems_status_array[teamname] = tempstring
            else:
                tempstring += "2"
                problems_status_array[teamname] = tempstring # Otherwise the submission is pending (works because the cell will just
                # be printed blank if there isnt an available submission for this problem/team combo yet

            print("tempstring")
            print(tempstring)
            print("problems status array: ")
            print(problems_status_array)
            print(problem_score_array)


    return render(request, 'contests/scoreboard.html', {'teams' : participants_string, 'problem_count' : problem_count_array,
		'problems' : problems, 'contest_title' : contest_title, 'problem_status_array' : problems_status_array, 'problem_score_array' : problem_score_array})
