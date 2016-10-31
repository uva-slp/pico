from django.shortcuts import render, redirect

from teams.forms import TeamForm, TeamJoinForm, TeamLeaveForm
from contests.forms import CreateContestForm
from contests.models import Contest
from teams.models import Team
from users.models import User
from contests.lib import diff as _diff

def home(request):
	return render(
		request,
		'contests/home.html',
		{'team_form': TeamForm(), 'team_join_form': TeamJoinForm(request), 'team_leave_form': TeamLeaveForm(request)})

def diff(request):
	emptylines = 'emptylines' in request.GET
	whitespace = 'whitespace' in request.GET

	fromlines = ['foo ', 'f ', '  fs  ', '', 'bar', 'flarp']
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

    #get information from form
	if request.method == 'POST':

            form = CreateContestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contests/home.html', {'form' : form})
        else:
            form = CreateContestForm()
        return render(request, 'contests/create_contest.html', {'form': form})

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