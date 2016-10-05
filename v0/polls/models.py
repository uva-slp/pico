import datetime

from django.db import models
from django.utils import timezone

#I don't want to delete this one in case it breaks the site
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
#this is the start of our actual tables
class Contest(models.Model):
    title = models.CharField(max_length=128, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.CharField(max_length=32, primary_key=True)
    def __str__(self):
        return self.title

class Question(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, primary_key=True)
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
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, primary_key=True)
    question_number = models.ForeignKey(Question, on_delete=models.CASCADE, primary_key=True)
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
