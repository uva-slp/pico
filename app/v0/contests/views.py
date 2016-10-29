from django.shortcuts import render, redirect

from teams.forms import TeamForm, TeamJoinForm, TeamLeaveForm
from .forms import CreateContestForm, CreateContestTemplate, CreateQuestionAnswer
from django.forms.formsets import formset_factory
from lib import diff as _diff
from django.urls import reverse

def home(request):
	return render(
		request,
		'contests/home.html',
		{'team_form': TeamForm(), 'team_join_form': TeamJoinForm(request), 'team_leave_form': TeamLeaveForm(request)})

def diff(request):
	fromlines = ['foo', 'bar', 'flarp']
	tolines = ['food', 'jip', 'bar', 'zoo', 'jaslkdfj;laskdjflasdlkflasdgflkjghkljcvkljadkjlfhkajsldfhlkawheuifyiasdhflkjashdjklfhkajsdhflkjashiudfyoiauwhelkfjhaslkjdfhklasjhdfkljashdkflj']

	html, numChanges = _diff.HtmlFormatter(fromlines, tolines).asTable()

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
			form.save()
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
