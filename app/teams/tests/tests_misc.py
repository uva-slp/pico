from django.test import TestCase

from teams.models import Team, Invite, JoinRequest
from users.models import User

class TeamTestCases(TestCase):

    fixtures = ['teams.json']

    def testTeamFixture(self):
        t = Team.objects.get(pk = 1)
        self.assertEqual(t.name, 'Team 1')
        t.name = 'wrong name'
        t.save()
    # Jamel
    def testTeamNameFilter(self):
        teams = Team.objects.all()
        c = Team(name = "testTeam")
        c.save()
        if(teams.filter(name="testTeam")) :
            self.assertEqual(c.name, "testTeam")
    # Jamel
    def testNumberofTeams(self):
        a = Team(name="team1")
        b = Team(name="team2")
        c = Team(name="team3")
        d = Team(name="team4")
        e = Team(name="team5")
        a.save()
        b.save()
        c.save()
        d.save()
        e.save()
        teams = Team.objects.all()
        teamnumber = teams.count()
        self.assertEqual(teamnumber, 6)

    # nathan
    def testTeamStr(self):
        team = Team(name="team")

        self.assertEqual(str(team), "team")


class InviteTestCases(TestCase):

    #jason 
    def testInviteCount(self):
        u1 = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        u2 = User(username='buddy2', password='jgd3hb222', first_name='123', email='buddy2@gmail.com')
        t = Team(name='team')
        u1.save()
        u2.save()
        t.save()
        i1 = Invite(team=t, user=u1)
        i2 = Invite(team=t, user=u2)
        i1.save()
        i2.save()
        invite_count = Invite.objects.all().count()
        self.assertEqual(invite_count, 2)

    #jason
    def testInviteIdentity(self):
        #we should change this, you shouldnt be able to invite yourself to a team you created
        u1 = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        t = Team(name='team')
        u1.save()
        t.save()
        t.members.add(u1)
        i = Invite(team=t, user=u1)
        i.save()
        invite_count = Invite.objects.all().count()
        self.assertEqual(invite_count, 1)

    #jason
    def testJoinRequest(self):
        u = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        t = Team(name='team')
        u.save()
        t.save()
        j = JoinRequest(team=t, user=u)
        j.save()
        join_request_count = JoinRequest.objects.all().count()
        self.assertEqual(join_request_count, 1)

    #jason
    def testJoinRequestIdentity(self):
        #we should change this, you shouldnt be able to send a join request to your own team
        u = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        t = Team(name='team')
        u.save()
        t.save()
        t.members.add(u)
        j = JoinRequest(team=t, user=u)
        j.save()
        join_request_count = JoinRequest.objects.all().count()
        self.assertEqual(join_request_count, 1)