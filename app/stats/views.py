from django.shortcuts import render
from contests.models import Participant, Submission
from teams.models import Team
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    participation = Participant.objects.filter(team__members__username=request.user.username).order_by('contest__date_created')
    contest_count = Participant.objects.filter(team__members__username=request.user.username).count()
    teams = Team.objects.filter(members__username=request.user.username).order_by('name')

    submissions = Submission.objects.filter(team__members__username=request.user.username).order_by('result')
    submissions_count = Submission.objects.filter(team__members__username=request.user.username).count()
    correct_submissions = 0

    for s in submissions:
        if s.result == 'YES':
            correct_submissions += 1

    teams_count = teams.count()
    teammates_count = 0
    best_team = None
    best_team_count = 0
    teammate_freq = {}
    favorite_teammates = []

    for t in teams:
        members = t.members.all()
        for m in members:
            if m.username != request.user.username:
                teammates_count += 1
                if m not in teammate_freq:
                    teammate_freq[m] = 1
                else:
                    teammate_freq[m] += 1
        team_correct_num = Submission.objects.filter(team__members__username=request.user.username).filter(result='YES').count()
        if team_correct_num > best_team_count:
            best_team_count = team_correct_num
            best_team = t

    for i in range(3):
        favorite_teammates.append(keywithmaxval(teammate_freq))
        if favorite_teammates[i] != None:
            del teammate_freq[favorite_teammates[i]]

    return render(request, 'stats/index.html', { 'participation' : participation,
                                                    'contest_count' : contest_count,
                                                    'teams' : teams,
                                                    'teams_count' : teams_count,
                                                    'teammates_count' : teammates_count,
                                                    'correct_submissions' : correct_submissions,
                                                    'best_team' : best_team,
                                                    'best_team_count' : best_team_count,
                                                    'favorite_teammates' : favorite_teammates})


def keywithmaxval(dic):
    """ a) create a list of the dict's keys and values; 
        b) return the key with the max value"""  
    v=list(dic.values())
    k=list(dic.keys())
    if len(v) > 0:
        return k[v.index(max(v))]
    else:
        return None
