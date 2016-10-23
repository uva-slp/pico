from django.db import models
from users.models import User, Team

class Contest(models.Model):
	title = models.CharField(max_length=128)
	date_created = models.DateTimeField(auto_now_add=True)
	creator = models.CharField(max_length=32)
	teams = models.ManyToManyField(Team)
	
	def __str__(self):
		return self.title

class Question(models.Model):
	number = models.IntegerField()
	name = models.CharField(max_length=2048)
	contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

	def __str__(self):
		return self.question_number + " " + self.question_text

class Submissions(models.Model):
	team = models.ForeignKey(Team)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now=True)
