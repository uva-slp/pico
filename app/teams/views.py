from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from common.decorators import anonymous_required
from .forms import TeamForm, TeamJoinForm, TeamLeaveForm

@login_required
def create_team(request):
	if request.method == 'POST':
		team_form = TeamForm(data=request.POST)

		if team_form.is_valid():
			team = team_form.save()
			team.members.add(request.user)
	
	return redirect(reverse('contests:home'))

@login_required
def join_team(request):
	if request.method == 'POST':
		team_join_form = TeamJoinForm(data=request.POST)

		if team_join_form.is_valid():
			team = team_join_form.cleaned_data['team']
			request.user.team_set.add(team)

	return redirect(reverse('contests:home'))

@login_required
def leave_team(request):
	if request.method == 'POST':
		team_leave_form = TeamLeaveForm(data=request.POST)

		if team_leave_form.is_valid():
			team = team_leave_form.cleaned_data['team']
			request.user.team_set.remove(team)
			if team.members.count() == 0:
				team.delete()

	return redirect(reverse('contests:home'))
