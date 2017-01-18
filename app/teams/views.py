from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from dal import autocomplete

from .models import Team
from .forms import TeamForm, TeamSelectForm, TeamSearchForm

@login_required
def index(request, team_id=None):
    current = None
    if team_id is not None:
        if Team.objects.filter(id=team_id).exists():
            current = Team.objects.get(id=team_id)
        else:
            return redirect(reverse('teams:index'))

    return render(
        request,
        'teams/index.html',
        {
            'current': current,
            'teams': request.user.teams.all(),
            'team_form': TeamForm(),
            'team_search_form': TeamSearchForm(),
        },
    )

@login_required
def create(request):
    if request.method == 'POST':
        team_form = TeamForm(data=request.POST)

        if team_form.is_valid():
            team = team_form.save()
            team.members.add(request.user)
            data = {
                'tab': render_to_string('teams/team-tab.html', {'team': team}, request),
                'panel': render_to_string('teams/team-panel.html', {'team': team}, request),
            }
            return JsonResponse(data, status=200)
    
        else:
            data = {
                'form': render_to_string('forms/horizontal.html', {'form': team_form}, request),
            }
            return JsonResponse(data, status=201)

    return redirect(reverse('teams:index'))

@login_required
def join(request):
    if request.method == 'POST':
        team_select_form = TeamSelectForm(data=request.POST)

        if team_select_form.is_valid():
            team = team_select_form.cleaned_data['team']
            team.members.add(request.user)

    return redirect(reverse('teams:index', kwargs={'team_id':team.id}))

@login_required
def leave(request):
    if request.method == 'POST':
        team_select_form = TeamSelectForm(data=request.POST)

        if team_select_form.is_valid():
            team = team_select_form.cleaned_data['team']
            team.members.remove(request.user)
            # if team.members.count() == 0:
            #     team.delete()
            return JsonResponse({}, status=200)

    return redirect(reverse('teams:index'))

@login_required
def get(request):
    if request.method == 'POST':
        team_search_form = TeamSearchForm(data=request.POST)

        if team_search_form.is_valid():
            team = team_search_form.cleaned_data['team']
            data = {
                'tab': render_to_string('teams/team-tab.html', {'team': team}, request),
                'panel': render_to_string('teams/team-panel.html', {'team': team}, request),
            }
            return JsonResponse(data, status=200)

        return JsonResponse({}, status=201)

    return redirect(reverse('teams:index'))

class TeamAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):     
        if not self.request.user.is_authenticated():
            return Team.objects.none()
        
        qs = Team.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        
        return qs
