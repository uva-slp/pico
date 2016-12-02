from django.db import models
from users.models import User
from teams.models import Team

'''
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
'''

class Contest(models.Model):
	title = models.CharField(max_length=128)
	date_created = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	languages = models.CharField(max_length=64)
	contest_length = models.CharField(max_length=8)
	time_penalty = models.CharField(max_length=4)
	autojudge_enabled = models.BooleanField(max_length=1, default=False)
	autojudge_review = models.CharField(max_length=128, null=True, blank=True)
	problem_description = models.FileField(upload_to='uploads/', null=True, blank=True)
	contest_admins = models.TextField()
	contest_participants = models.TextField()

	def __str__(self):
		return self.title

class Problem(models.Model):
	number = models.IntegerField(null=True)
	name = models.CharField(max_length=2048, null=True, blank=True)
	solution = models.FileField(upload_to='uploads/', null=True, blank=True)
	input_description = models.CharField(max_length=128, null=True, blank=True)
	output_description = models.CharField(max_length=128, null=True, blank=True)
	sample_input = models.FileField(upload_to='uploads/', null=True, blank=True)
	sample_output = models.FileField(upload_to='uploads/', null=True, blank=True)
	contest = models.ForeignKey(Contest, null=True, blank=True, on_delete=models.CASCADE)

class Participant(models.Model):
	contest = models.ForeignKey(Contest, null=True, blank=True, on_delete=models.CASCADE)
	team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
	score = models.IntegerField

class Submission(models.Model):
	run_id = models.AutoField(primary_key = True)
	team = models.ForeignKey(Team, null = True)
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)
	code_file = models.FileField(upload_to='uploads/', null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=True)
	original_filename = models.CharField(max_length=128, null=True, blank=True)

	JUDGE_RESULT = (
		('YES', 'Yes'),
		('WRONG', 'Wrong Answer'),
		('OFE', 'Output Format Error'),
		('IE', 'Incomplete Error'),
		('EO', 'Excessive Output'),
		('CE', 'Compilation Error'),
		('RTE', 'Run-Time Error'),
		('TLE', 'Time-Limit Exceeded'),
		('OTHER', 'Other-Contact Staff'),
	)

	SUBMISSION_STATE_CHOICES = (
		('NEW', 'New'),
		('YES', 'Yes'),
		('NO', 'No'),
	)
	state = models.CharField(max_length=20, choices=SUBMISSION_STATE_CHOICES, default='NEW')
	result = models.CharField(max_length=20, choices=JUDGE_RESULT, null=True)

	def __str__(self):
		return str(self.run_id)

class ContestTemplate(models.Model):
	title = models.CharField(max_length=128)
	creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	languages = models.CharField(max_length=64)
	contest_length = models.CharField(max_length=8)
	time_penalty = models.CharField(max_length=4)
	autojudge_enabled = models.BooleanField(max_length=1, default=False)
	autojudge_review = models.CharField(max_length=128, null=True, blank=True)
	contest_admins = models.TextField()
	contest_participants = models.TextField()

	def __str__(self):
		return self.title
