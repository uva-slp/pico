from django.test import TestCase

from teams.models import Team

class TeamTestCases(TestCase):

    fixtures = ['teams.json']

    def testTeamFixture(self):
        t = Team.objects.get(pk = 1)
        self.assertEqual(t.name, 'Team 1')
        t.name = 'wrong name'
        t.save()

    def testTeamNameFilter(self):
        teams = Team.objects.all()
        c = Team(name = "testTeam")
        c.save()
        if(teams.filter(name="testTeam")) :
            self.assertEqual(c.name, "testTeam")

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

    def testTeamStr(self):
        team = Team(name="team")

        self.assertEqual(str(team), "team")
