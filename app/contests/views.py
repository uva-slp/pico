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
from teams.models import Team
from .models import Participant
from users.models import User


#Imports used for code compilation/execution
import os
import subprocess, shlex
import tempfile
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))


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

def diff(request):
	emptylines = 'emptylines' in request.GET
	whitespace = 'whitespace' in request.GET

	fromlines = ['foo ', 'f ', '  fs  ', '   ', 'bar', 'flarp']
	tolines = ['foo', 'bar', 'zoo']

	html, numChanges = _diff.HtmlFormatter(fromlines, tolines, emptylines, whitespace).asTable()

	return render(
		request,
		'contests/diff.html',
		{'diff_table': html, 'numChanges': numChanges})

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
		#grab information from form
		form = CreateContestForm(request.POST, request.FILES)
		#qa_formset = CreateProblem(request.POST)

		qa_formset = QAFormSet(request.POST, request.FILES)
		if form.is_valid() and qa_formset.is_valid():
			problem_desc = Contest(problem_description=request.FILES['problem_description'])
			problem_desc.save()
			contest = form.save()
			contest.creator = request.user
			contest.save()

			contest_id = form.id

			for qa_form in qa_formset:
				solution = qa_form.cleaned_data.get('solution')
				input_desc = qa_form.cleaned_data.get('input_description')
				output_desc = qa_form.cleaned_data.get('output_description')
				sample_input = qa_form.cleaned_data.get('sample_input')
				sample_output = qa_form.cleaned_data.get('sample_output')
				contest = qa_form.cleaned_data.get('title')

				p = Problem(
					solution=solution, input_description=input_desc,
					output_description=output_desc, sample_input=sample_input,
					sample_output=sample_output, contest_id=contest_id)

				p.save()

			return redirect(reverse('contests:home'))
			# return render(request, 'contests/home.html', {'form': form, 'qa_formset': qa_formset})
	else:
		form = CreateContestForm()
		QAFormSet = formset_factory(CreateProblem)
		qa_formset = QAFormSet()
	return render(request, 'contests/create_contest.html', {'form': form, 'qa_formset': qa_formset})


@login_required
def displayContest(request, contest_id):
	contest_data = Contest.objects.get(id=contest_id)
	problems = contest_data.problem_set.all()
	is_judge = False
	# TODO: Right now this only check contest creator. Need to update to all judges
	if request.user == contest_data.creator:
		is_judge = True

	# TODO: Update to participants after contest model updated.
	teams = Team.objects.all()

	return render(
		request,
		'contests/contest.html',
		{'contest_data': contest_data, 'contest_problems': problems, 'is_judge': is_judge,
			'contest_teams': teams}
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
				{'contest_data': contest_data, 'is_judge': True,
					'submission': current_submission, 'form': form}
			)

	return render(
		request,
		'contests/judge.html',
		{'contest_data': contest_data, 'is_judge': False}
	)


def choose_problem(request):
    all_problems = Problem.objects.all()
    return render(request, 'contests/choose_problem.html', {'problems': all_problems})


def upload_code(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    if request.method == 'POST':
        form = UploadCodeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            execute_code(request.FILES['code_file'], form.instance.id)
            return render(request, 'contests/uploaded.html')
    else:
        form = UploadCodeForm(initial = {'problem': problem})
    return render(request, 'contests/upload_page.html', {'form': form, 'problem': problem})


#Returns True if executed successfully, false otherwise
def execute_code(file, submission_id):
    file_name = file.name
    #Check if it's a Java file:
    if file_name.endswith('.java'):
        run_java(file, submission_id)
        return True
    #Check if it's a c++ file:
    cpp_extensions = ['.cpp', '.cc', '.C', '.cxx', '.c++']
    for extension in cpp_extensions:
        if file_name.endswith(extension):
            run_cpp(file, submission_id)
            return True
    #If it didn't have a proper extensions, can't compile it:
    return False


def run_java(file, submission_id):
    temp_dirpath = tempfile.mkdtemp()
    file_name = file.name
    with open(os.path.join(temp_dirpath, file_name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    retcode = subprocess.call("javac " + os.path.join(temp_dirpath, file_name), shell=True)
    #compilation_args = shlex.split("javac " + os.path.join(temp_dirpath, file_name))
    #result = subprocess.Popen(compilation_args)
    compiled_file = os.path.splitext(file_name)[0]
    #retcode = subprocess.call("java -cp " + temp_dirpath + " " + compiled_file + ' > ' + os.path.join(temp_dirpath, 'output.txt'), shell=True)
    output = subprocess.check_output("java -cp " + temp_dirpath + " " + compiled_file, shell=True)
    print(output)
    #execution_args = shlex.split("java -cp " + temp_dirpath + " " + compiled_file)
    #retcode = subprocess.Popen(execution_args)
    shutil.rmtree(temp_dirpath)


def run_cpp(file, submission_id):
    temp_dirpath = tempfile.mkdtemp()
    file_name = file.name
    with open(os.path.join(temp_dirpath, file_name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    retcode = subprocess.call("/usr/bin/g++ " + os.path.join(temp_dirpath, file_name) + " -o " + os.path.join(temp_dirpath, 'a.out'), shell=True)
    if retcode:
        print("failed to compile " + file_name)
    #retcode = subprocess.call(os.path.join(temp_dirpath, './a.out') + ' > ' + os.path.join(path, 'output.txt'), shell=True)
    output = subprocess.check_output(os.path.join(temp_dirpath, './a.out'), shell=True)
    print(output)
    shutil.rmtree(temp_dirpath)

def scoreboard(request):
    # Get number of teams for scoreboard, scores for each team at that moment, logos, questions and whether theyve been attempted, solve, or neither
    userPK = request.user.pk

    # Get participant based off of active team? Then pull contest based on that? Then pull other teams and view scores

    print("Current User PK: ")
    print(request.user.pk)
    allcontests = Contest.objects.all() #get contest objects
    allteams = Team.objects.all() #get team objects
    allteams = allteams.filter(members=userPK) #get teams that have current user in them
    print(allcontests)
    allcontests = allcontests.filter(contest_participants=allteams.values('name')) #Get contest with user's team

    print("filter:")
    print("teams:")
    print(allteams)
    print("contest:")
    print(allcontests)

    #allteams.filter(name=)
    currentTeamName = "Get current team name" #Get requesting team's name
    currentContestTitle = "testcontest" #get requesting team's current contest

    numberofteams = 0
    teamname = allteams.filter(name=currentTeamName)
    contestname = allcontests.filter(title = currentContestTitle) # Grab current contest

    #for team in allcontests.teams :
    #    numberofteams += 1
    #    print(numberofteams)

    # get query_results.numberofteams
    # for(team in query_results.teams) { scores += team.score
    # return object containing array of teams

    return render(request, 'contests/scoreboard.html', {'teams' : allteams})
