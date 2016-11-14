from django.db import models
from users.models import User
from teams.models import Team

class Contest(models.Model):
	title = models.CharField(max_length=128)
	date_created = models.DateTimeField(auto_now_add=True)
	creator = models.CharField(max_length=32)
	teams = models.ManyToManyField(Team)
	languages = models.CharField(max_length=100)
	contest_length = models.CharField(max_length=10)
	autojudge = models.CharField(max_length=10)
	contest_admins = models.CharField(max_length=100, null=True)
	contest_participants = models.CharField(max_length=200, null=True)
	
	def __str__(self):
		return self.title

class Question(models.Model):
	number = models.IntegerField()
	name = models.CharField(max_length=2048)
	contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.number)


class Submission(models.Model):
	team = models.ForeignKey(Team, null = True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	code_file = models.FileField(upload_to='uploads/', null=True, blank=False)
	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.submission_id)


class ContestTemplate(models.Model):
	title = models.CharField(max_length=128)
	date_created = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	languages = models.CharField(max_length=64)
	contest_length = models.CharField(max_length=8)
	time_penalty = models.CharField(max_length=4)
	autojudge_enabled = models.BooleanField(max_length=1)
	autojudge_review = models.CharField(max_length=128)
	problem_description = models.CharField(max_length=128)
	contest_admins = models.TextField()
	contest_participants = models.TextField()

	def __str__(self):
		return self.title

class Problem(models.Model):
	solution = models.FileField(max_length=128)
	input_description = models.CharField(max_length=128)
	output_description = models.CharField(max_length=128)
	sample_input = models.FileField(max_length=128)
	sample_output = models.FileField(max_length=128)
	contest = models.ForeignKey(ContestTemplate, null=True, blank=True, on_delete=models.CASCADE)

class Participant(models.Model):
	contest = models.OneToOneField(ContestTemplate)
	team = models.OneToOneField(Team)
	score = models.IntegerField

class Submission(models.Model):
	run_id = models.IntegerField(null=True)
	team = models.ForeignKey(Team, null = True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)
	code_file = models.FileField(upload_to='uploads/', null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=True)
	SUBMISSION_STATE_CHOICES = (
		('NEW', 'New'),
		('YES', 'Yes'),
		('NO', 'No'),
	)
	state = models.CharField(max_length=20, choices=SUBMISSION_STATE_CHOICES, default='NEW')

	def __str__(self):
		return str(self.run_id)
