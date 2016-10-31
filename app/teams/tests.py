from django.test import TestCase
from models import Contest, User, Team

# Create your tests here.
class ContestTestCases(TestCase):

    def testContestCreation(self):
        c = Contest(title = "super contest", creator = "james")
        self.assertEqual(c.title, "super contest")
        self.assertEqual(c.creator, "james")

    def testTeamNameFilter(self):
        teams = Team.objects.all()
        c = Team(name = "testTeam")
        c.save()
        teams.filter(name="testTeam")
        self.assertEqual(c.name, teams.filter(name="testTeam"))

    def testContestName(self):
        c = Contest(title="testContest")
        c.save()
        contests = Contest.objects.all()
        contests.filter(title="testContest")
        self.assertEqual(c.title, contests.filter(title="testContest"))

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
        self.assertEqual(teamnumber, 5)


    def testNumberofContests(self):
        a = Contest(title="contest1")
        b = Contest(title="contest1")
        c = Contest(title="contest1")
        d = Contest(title="contest1")
        e = Contest(title="contest1")
        a.save()
        b.save()
        c.save()
        d.save()
        e.save()
        contests = Contest.objects.all()
        teamnumber = contests.count()
        self.assertEqual(teamnumber, 5)
