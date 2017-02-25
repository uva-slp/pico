from django.db import models
from django.utils import timezone

from users.models import User
from teams.models import Team

from datetime import datetime, timedelta

class ContestManager(models.Manager):
	def pending(self):
		pending_contests = set()
		for contest in super(ContestManager, self).get_queryset():
			if contest.contest_start is None:
				pending_contests.add(contest)
		return pending_contests

	def active(self):
		active_contests = set()
		for contest in super(ContestManager, self).get_queryset():
			if contest.contest_start is not None and contest.contest_end() > timezone.now():
				active_contests.add(contest)
		return active_contests
	
	def past(self):
		past_contests = set()
		for contest in super(ContestManager, self).get_queryset():
			if contest.contest_start is not None and contest.contest_end() <= timezone.now():
				past_contests.add(contest)
		return past_contests

class Contest(models.Model):
	title = models.CharField(max_length=128)
	date_created = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="contest_creator")
	languages = models.CharField(max_length=64)
	contest_length = models.DateTimeField(null=True, blank=True)
	contest_start = models.DateTimeField(null=True, blank=True)
	time_penalty = models.DateTimeField(null=True, blank=True)
	autojudge_enabled = models.BooleanField(max_length=1, default=False)
	autojudge_review = models.CharField(max_length=128, null=True, blank=True)
	problem_description = models.FileField(upload_to='uploads/', null=True, blank=True)
	contest_admins = models.ManyToManyField(User, related_name="contest_admins")
	contest_participants = models.TextField()

	objects = ContestManager()

	def contest_end(self):
		if self.contest_start is None:
			return datetime.max.replace(tzinfo=timezone.utc)
		return self.contest_start + timedelta(seconds=self.contest_length.hour*3600+self.contest_length.minute*60)

	def time_remaining(self):
		if self.contest_start is None:
			return "Not started"
		seconds = (self.contest_end() - timezone.now()).seconds
		return "%d:%02d:%02d remaining"%(seconds//3600, seconds%3600//60, seconds%60)

	def __str__(self):
		return self.title

class Problem(models.Model):
	number = models.IntegerField(null=True)
	name = models.CharField(max_length=2048, null=True, blank=True)
	solution = models.FileField(upload_to='uploads/', null=True, blank=True)
	program_input = models.FileField(upload_to='uploads/', null=True, blank=False)
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

class Notification(models.Model):
	submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

class ContestTemplate(models.Model):
	title = models.CharField(max_length=128)
	creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="contesttemplate_creator")
	languages = models.CharField(max_length=64)
	contest_length = models.CharField(max_length=8)
	time_penalty = models.CharField(max_length=4)
	autojudge_enabled = models.BooleanField(max_length=1, default=False)
	autojudge_review = models.CharField(max_length=128, null=True, blank=True)
	contest_admins = models.ManyToManyField(User, related_name="contesttemplate_admins")
	contest_participants = models.TextField()

	def __str__(self):
		return self.title