from django.shortcuts import render, redirect

from app.teams.forms import TeamForm, TeamJoinForm, TeamLeaveForm
from .models import Question
from .forms import CreateContestForm, CreateContestTemplate, CreateQuestionAnswer, UploadCodeForm
from django.forms.formsets import formset_factory
from django.urls import reverse
from .lib import diff as _diff
from .models import Contest
from app.teams.models import Team


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
		{'team_form': TeamForm(), 'team_join_form': TeamJoinForm(request), 'team_leave_form': TeamLeaveForm(request)})

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

def createTemplate(request):

	if request.method == 'POST':
		#grab information from form
		form = CreateContestTemplate(request.POST)

		#QAFormSet = formset_factory(CreateQuestionAnswer)
		#qa_formset = QAFormSet()
		if form.is_valid():
			# and qa_formset.is_valid():
			form.save()

			questions = []
			answers = []

			#for qa_form in qa_formset:
			#	problem_desc = qa_form.cleaned_data.get('problem_desc')
			#	solution = qa_form.cleaned_data.get('solution')

			#	if problem_desc and solution:
			#		questions.append()
			#		answers.append()

			return redirect(reverse('contests:home'))
			# return render(request, 'contests/home.html', {'form': form, 'qa_formset': qa_formset})
	else:
		form = CreateContestTemplate()
		QAFormSet = formset_factory(CreateQuestionAnswer)
		qa_formset = QAFormSet()
	return render(request, 'contests/create_template.html', {'form': form, 'qa_formset': qa_formset})


def choose_question(request):
    all_questions = Question.objects.all()
    return render(request, 'contests/choose_question.html', {'questions': all_questions})


def upload_code(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = UploadCodeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            execute_code(request.FILES['code_file'], form.instance.id)
            return render(request, 'contests/uploaded.html')
    else:
        form = UploadCodeForm(initial = {'question': question})
    return render(request, 'contests/upload_page.html', {'form': form, 'question': question})


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
    allcontests = Contest.objects.all() #get contest objects
    allteams = Team.objects.all() #get team objects
    #allteams.filter(name=)
    currentTeamName = "Get current team name" #Get requesting team's name
    currentContestTitle = "newcontests" #get requesting team's current contest
    numberofteams = 0
    teamname = allteams.filter(name=currentTeamName)
    contestname = allcontests.filter(title = currentContestTitle) # Grab current contest
    print(allcontests)
    print(contestname)

    #for team in allcontests.teams :
    #    numberofteams += 1
    #    print(numberofteams)

    # get query_results.numberofteams
    # for(team in query_results.teams) { scores += team.score
    # return object containing array of teams


    return render(request, 'contests/scoreboard.html', {'teams' : numberofteams})