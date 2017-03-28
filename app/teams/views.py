from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from dal import autocomplete

from .models import Team, Invite, JoinRequest
from .forms import TeamForm, TeamSelectForm, TeamSearchForm, InviteForm, JoinRequestForm
from users.forms import UserSearchForm

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
            'user_search_form': UserSearchForm(),
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

            if request.user not in team.members.all():
                if team.public or Invite.objects.filter(team=team, user=request.user).exists():
                    team.members.add(request.user)
                    Invite.objects.filter(team=team, user=request.user).delete()
                    JoinRequest.objects.filter(team=team, user=request.user).delete()
                else:
                    JoinRequest(team=team, user=request.user).save()

    return redirect(reverse('teams:index', kwargs={'team_id':team.id}))

@login_required
def invite(request, action):
    if request.method == 'POST':
        if action == 'send':
            team_select_form = TeamSelectForm(data=request.POST)
            user_select_form = UserSearchForm(data=request.POST)

            if team_select_form.is_valid() and user_select_form.is_valid():
                team = team_select_form.cleaned_data['team']
                user = user_select_form.cleaned_data['user']

                if request.user in team.members.all():
                    if user in team.members.all():
                        # User already on team
                        pass
                    elif Invite.objects.filter(team=team, user=user).exists():
                        # Invite already exists
                        pass
                    else:
                        Invite(team=team, user=user).save()
                else:
                    # User does not have permission to send invite
                    pass    
            
                return redirect(reverse('teams:index', kwargs={'team_id':team.id}))            

        elif action == 'accept':
            return join(request)

        elif action == 'decline':
            team_select_form = TeamSelectForm(data=request.POST)

            if team_select_form.is_valid():
                team = team_select_form.cleaned_data['team']

                if Invite.objects.filter(team=team, user=request.user).exists():
                    Invite.objects.filter(team=team, user=request.user).delete()

                return redirect(reverse('teams:index', kwargs={'team_id':team.id}))

        elif action == 'cancel':
            invite_form = InviteForm(data=request.POST)

            if invite_form.is_valid():
                invite = invite_form.cleaned_data['invite']

                if request.user in invite.team.members.all():
                    invite.delete()

                return redirect(reverse('teams:index', kwargs={'team_id':invite.team.id}))

    return redirect(reverse('teams:index'))

@login_required
def join_request(request, action):
    if request.method == 'POST':
        print(request.POST)
        join_request_form = JoinRequestForm(data=request.POST)

        if join_request_form.is_valid():
            join_request = join_request_form.cleaned_data['request']

            if request.user in join_request.team.members.all():
                if action == 'accept':
                    join_request.team.members.add(join_request.user)
                    join_request.delete()
                    Invite.objects.filter(team=join_request.team, user=join_request.user).delete()
                elif action == 'decline':
                    join_request.delete()
            elif request.user == join_request.user and action == 'cancel':
                join_request.delete()

            return redirect(reverse('teams:index', kwargs={'team_id':join_request.team.id}))

    return redirect(reverse('teams:index'))

@login_required
def leave(request):
    if request.method == 'POST':
        team_select_form = TeamSelectForm(data=request.POST)

        if team_select_form.is_valid():
            team = team_select_form.cleaned_data['team']
            team.members.remove(request.user)
            if team.members.count() == 0:
                team.delete()
            return JsonResponse({}, status=200)

    return redirect(reverse('teams:index'))

@login_required
def is_public(request):
    if request.method == 'POST':
        print(request.POST)
        team_select_form = TeamSelectForm(data=request.POST)

        if team_select_form.is_valid():
            team = team_select_form.cleaned_data['team']

            if request.POST.get('public', 'off') == 'on':
                team.public = True
            else:
                team.public = False
            team.save()

            return JsonResponse({'public': team.public})

        return redirect(reverse('teams:index', kwargs={'team_id':team.id}))

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
