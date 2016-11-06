from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from dal import autocomplete

from .models import Team
from .forms import TeamForm, TeamJoinForm, TeamLeaveForm

@login_required
def create(request):
	if request.method == 'POST':
		team_form = TeamForm(data=request.POST)

		if team_form.is_valid():
			team = team_form.save()
			team.members.add(request.user)
	
	return redirect(reverse('contests:home'))

@login_required
def join(request):
	if request.method == 'POST':
		team_join_form = TeamJoinForm(data=request.POST)

		if team_join_form.is_valid():
			team = team_join_form.cleaned_data['team']
			team.members.add(request.user)

	return redirect(reverse('contests:home'))

@login_required
def leave(request):
	if request.method == 'POST':
		team_leave_form = TeamLeaveForm(data=request.POST)

		if team_leave_form.is_valid():
			team = team_leave_form.cleaned_data['team']
			team.members.remove(request.user)
			if team.members.count() == 0:
				team.delete()

	return redirect(reverse('contests:home'))

class TeamAutocomplete(autocomplete.Select2QuerySetView):

	def get_queryset(self):		
		if not self.request.user.is_authenticated():
			return Team.objects.none()
		
		qs = Team.objects.all()
		if self.q:
			qs = qs.filter(name__istartswith=self.q)


		queryType = int(self.kwargs.get('type', 0))
		if queryType == 0:
			return qs
		if queryType == 1: # join
			return qs.exclude(members=self.request.user)
		if queryType == 2: # leave
			return qs.filter(members=self.request.user)
		
		return qs
