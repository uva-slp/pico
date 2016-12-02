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
from .models import Participant
from users.models import User
from datetime import datetime
from django.utils import timezone

#To render multiple forms on a contest page (since there are multiple problems in a contest)
from django.forms.formsets import formset_factory

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
			'contests_created': Contest.objects.all(),
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

'''
def create(request):
    #boolean to see if the contest was successfully created
    #initally false, code will make it true it successful
    #successfully_created_contest = False
    #check to see if the page was loaded with POST request data

    if request.method == 'POST':
        #grab information from form
        form = CreateContestForm(request.POST)
        if form.is_valid():
            c = Contest()
            c.title = form.title
            c.creator = 'user'
            c.languages = form.languages
            c.length = form.length
            c.autojudge = form.autojudge
            c.save()
            return render(request, 'contests/home.html', {'form' : form})
    else:
        form = CreateContestForm()
    return render(request, 'contests/create_contest.html', {'form': form})
'''

def create(request):

	QAFormSet = formset_factory(CreateProblem)
    
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


@login_required
def displayContest(request, contest_id):
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

	contest_data = Contest.objects.get(id=contest_id)

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
                        
	return render( request, 'contests/contest.html', {'contest_data': contest_data, 'contest_problems': problems, 'is_judge': is_judge, 'contest_teams': contest_participants, 'submission_attempts': submission_attempts, 'submission_status': status, 'color_states': color_states, 'problem_form_pairs' : problem_form_pairs })


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


# Method for getting nearest datetime
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def scoreboard(request):
    userPK = request.user.pk # Get users primary key

    allcontests = Contest.objects.all() # Get all contest objects
    allteams = Team.objects.all() # Get all team objects
    allteams = allteams.filter(members=userPK) # Get teams that have current user in them
    print("teams with requesting user")
    print(allteams)

    testcontests = allcontests

    team_contests_array = [] # Holds all contests based on each users team

    for team in allteams.iterator(): # Loop to filter possible contest pool down by each team the user is a part of
        print("teamloop")
        print(team.name)
        testcontests = testcontests.filter(contest_participants__contains=team.name)
        #print(testcontests)
        team_contests_array.append(testcontests)
        #print(allcontests)

    #print(team_contests_array)
    requestdatetime = datetime.now(timezone.utc) # Get current time to match with most recently joined contest based on the user's team
    print(requestdatetime)

    testnearestdate = []
    testnearestarray = []

    for index in team_contests_array:
        for contest in index:
            testnearestdate.append(contest.date_created)
            #print(contest)
        testnearestarray.append(nearest(testnearestdate, requestdatetime)) # Get nearest date for each grouping regarding team

    # testnearestarray now contains contest times created for the most recently created contests under each team relevant to the user requesting the scoreboard
    print("testnearestarray: ")
    print(testnearestarray)


    #print "allcontests before filter"
    #print(allcontests)
    #print(allteams.values('name'))
    allcontests = allcontests.filter(contest_participants__in="team3") # Get all contests with user's teams
    #print("allcontests after filtering by user's teams")
    #print(allcontests)

    nearestdate = []

    for contest in allcontests.iterator(): # Create tuple of all contests with this user/team
        nearestdate.append(contest.date_created)

    mostrecentcontestdate = nearest(nearestdate, requestdatetime) # Get whatever contest date is nearest to request date
    mostrecentcontest = allcontests.filter(date_created=mostrecentcontestdate) # Filter queryset by nearest date created to get relevant contest for scoreboard request
    problems = Problem.objects.all()
    problems = problems.filter(contest=mostrecentcontest)
    problem_count = 0
    for problem in problems :
        problem_count += 1
        print("problem:")
        print(problem.name)

    print("most recent contest:")
    print(mostrecentcontest)
    for contest in mostrecentcontest: # Should be 1 contest
        print("Participant:")
        print(contest.contest_participants)

    return render(request, 'contests/scoreboard.html', {'teams' : allteams, 'problem_count' : problem_count, 'problems' : problems})
