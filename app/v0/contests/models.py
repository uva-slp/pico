from django.db import models
from django.contrib.auth.models import User, Group

class Contest(models.Model):
	title = models.CharField(max_length=128, primary_key=True)
	dateCreated = models.DateTimeField(auto_now_add=True)
	creator = models.CharField(max_length=32, primary_key=True)
	teams = models.ManyToManyField(Group)
	
	def __str__(self):
		return self.title

class Question(models.Model):
	number = models.IntegerField()
	name = models.CharField(max_length=2048)
	contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

	def __str__(self):
		return self.question_number + " " + self.question_text

class Submissions(models.Model):
	team = models.ForeignKey(Group)
	contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now=True)
