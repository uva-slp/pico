from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from teams.models import Team
from users.models import User
from contests.models import Contest, Problem, ContestTemplate, Participant, Submission, Notification
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import Http404
from django.template.loader import render_to_string
import os

def index(request):

    if request.user.is_authenticated():
        participation = Participant.objects.filter(team__members__username=request.user.username).order_by('contest__date_created')
        contest_count = Participant.objects.filter(team__members__username=request.user.username).count()
        teams = Team.objects.filter(members__username=request.user.username).order_by('name')
        teams_count = teams.count()
        teammates_count = 0
        for t in teams:
            members = t.members.all()
            for m in members:
                if m.username != request.user.username:
                    teammates_count += 1
        return render(request, 'stats/index.html', { 'participation' : participation, 
                                                        'contest_count' : contest_count,
                                                        'teams' : teams,
                                                        'teams_count' : teams_count,
                                                        'teammates_count' : teammates_count})
    else:
        return render(request, 'stats/index.html')

# Create your views here.
