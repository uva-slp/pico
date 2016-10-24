from django.shortcuts import render, redirect

from teams.forms import TeamForm, TeamJoinForm, TeamLeaveForm
from contests.forms import CreateContestForm
from lib import diff as _diff

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