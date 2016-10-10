from django.db import models

class Contest(models.Model):
    title = models.CharField(max_length=128, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.CharField(max_length=32, primary_key=True)
    def __str__(self):
        return self.title

class Question(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    question_number = models.IntegerField(primary_key=True)
    question_text = models.CharField(max_length=2048)
    submission = models.CharField(max_length=128) #title of document submission
    def __str__(self):
        return self.question_number + "\n" + self.question_text

class Team(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    submission = models.CharField(max_length=128) #title of document submission
    def __str__(self):
        return self.name

class Submissions(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    question_number = models.ForeignKey(Question, on_delete=models.CASCADE)
    submission = models.CharField(max_length=128) #title of the document submission
    def __str__(self):
        return "CONTEST: " + self.contest + "\n" + "TEAM: " + self.team + "\n" + "QUESTION: " + self.question_number + "\n" + "SUBMISSION: " + self.submission

class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=64)
    privilege = models.CharField(max_length=16)
    team = models.ForeignKey(Team)
    def __str__(self):
        return self.username
