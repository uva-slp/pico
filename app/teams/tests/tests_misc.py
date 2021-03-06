from django.test import TestCase

from teams.models import Team, Invite, JoinRequest
from users.models import User


class TeamTestCases(TestCase):

    fixtures = ['users.json', 'teams.json']

    # Jamel
    def testTeamFixture(self):
        t = Team.objects.get(pk=1)
        self.assertEqual(t.name, 'Team 1')
        t.name = 'wrong name'
        t.save()

    # Jamel
    def testTeamNameFilter(self):
        teams = Team.objects.all()
        c = Team(name="testTeam")
        c.save()
        if(teams.filter(name="testTeam")) :
            self.assertEqual(c.name, "testTeam")

    # Jamel
    def testNumberofTeams(self):
        teams = Team.objects.all()
        team_count_before = teams.count()

        a = Team(name="test team1")
        b = Team(name="test team2")
        c = Team(name="test team3")
        d = Team(name="test team4")
        e = Team(name="test team5")
        a.save()
        b.save()
        c.save()
        d.save()
        e.save()

        teams = Team.objects.all()
        team_count_after = teams.count()

        self.assertEqual(team_count_after, team_count_before + 5)

    # nathan
    def testTeamStr(self):
        team = Team(name="team")

        self.assertEqual(str(team), "team")


class InviteTestCases(TestCase):

    # jason
    def test_invite_count(self):
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

    # jason
    def test_invite_identity(self):
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

    # jason
    def test_join_request_creation(self):
        u = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        t = Team(name='team')
        u.save()
        t.save()
        j = JoinRequest(team=t, user=u)
        j.save()
        join_request_count = JoinRequest.objects.all().count()
        self.assertEqual(join_request_count, 1)

    # jason
    def test_join_request_identity(self):
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

    # jason
    def test_join_request_sent(self):
        u = User(username='buddy1', password='jgd3hb111', email='buddy1@gmail.com')
        t = Team(name='team')
        u.save()
        t.save()
        j = JoinRequest(team=t, user=u)
        j.save()
        self.assertEqual(j.user, u)
