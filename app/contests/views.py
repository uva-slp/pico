from django.shortcuts import render, redirect

from teams.forms import TeamForm, TeamJoinForm, TeamLeaveForm
from organizations.forms import OrganizationForm, OrganizationJoinForm, OrganizationLeaveForm
from .models import Question, Problem, ContestTemplate
from .forms import CreateContestForm, CreateContestTemplate, CreateProblem, UploadCodeForm
from django.forms.formsets import formset_factory
from django.urls import reverse
from .lib import diff as _diff
from .lib import execution as exe
from .models import Contest
from teams.models import Team


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
			'contests_created': ContestTemplate.objects.all()
		}
	)


def choose_question(request):
    all_questions = Question.objects.all()
    return render(request, 'contests/choose_question.html', {'questions': all_questions})


def upload_code(request, question_id):
    question = Question.objects.get(id=question_id)
    form = UploadCodeForm(initial = {'question': question})
    return render(request, 'contests/upload_page.html', {'form': form, 'question': question})


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

	QAFormSet = formset_factory(CreateProblem)

	if request.method == 'POST':
		#grab information from form
		form = CreateContestTemplate(request.POST)
		#qa_formset = CreateProblem(request.POST)

		qa_formset = QAFormSet(request.POST)
		if form.is_valid() and qa_formset.is_valid():
			form = form.save()

			contest_id = form.id

			# questions = []
			# answers = []

			for qa_form in qa_formset:
				solution = qa_form.cleaned_data.get('solution')
				input_desc = qa_form.cleaned_data.get('input_description')
				output_desc = qa_form.cleaned_data.get('output_description')
				sample_input = qa_form.cleaned_data.get('sample_input')
				sample_output = qa_form.cleaned_data.get('sample_output')

				p = Problem(
					solution=solution, input_description=input_desc,
					output_description=output_desc, sample_input=sample_input,
					sample_output=sample_output, contest_id=contest_id)
				p.save();
				#p.solution = solution
				#p.input_description = input_descr
				#p.output_description = output_descr
				#p.sample_input = sample_input
				#p.sample_output = sample_output
				#p.contest_id = 1

			#	if problem_desc and solution:
			#		questions.append()
			#		answers.append()

			return redirect(reverse('contests:home'))
			# return render(request, 'contests/home.html', {'form': form, 'qa_formset': qa_formset})
	else:
		form = CreateContestTemplate()
		QAFormSet = formset_factory(CreateProblem)
		qa_formset = QAFormSet()
	return render(request, 'contests/create_template.html', {'form': form, 'qa_formset': qa_formset})


def displayContest(request, contest_id):
	contest_data = ContestTemplate.objects.get(id=contest_id)
	problems = contest_data.problem_set.all()
	submissions = []
	for p in problems:
		submissions += list(p.submission_set.all())
	submissions.sort(key=lambda x: x.timestamp)

	return render(
		request,
		'contests/contest.html',
		{'contest_data': contest_data, 'contest_problems': problems, 'contest_submissions': submissions}
	)


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

    #for team in allcontests.teams :
    #    numberofteams += 1
    #    print(numberofteams)

    # get query_results.numberofteams
    # for(team in query_results.teams) { scores += team.score
    # return object containing array of teams


    return render(request, 'contests/scoreboard.html', {'teams' : numberofteams})
