from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class Contest(models.Model):
	title = models.CharField(max_length=128, default="contest", unique=True)
	dateCreated = models.DateTimeField(null=True, blank=True)
	creator = models.CharField(max_length=32, null=True, blank=True)
	teams = models.ManyToManyField(Group, blank=True)
	
	def __str__(self):
		return self.title

class Question(models.Model):
	number = models.IntegerField(null=True, blank=True)
	name = models.CharField(max_length=2048, null=True, blank=True)
	contest = models.ForeignKey(Contest, null=True, blank=True, on_delete=models.CASCADE)
        problem = models.FileField(null=True, blank=True)
        test_file = models.FileField(null=True, blank=True)
        expected_output = models.FileField(null=True, blank=True)

	def __str__(self):
		return str(self.number) + ": " + self.name
