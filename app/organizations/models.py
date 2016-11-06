from django.db import models

from users.models import User
from teams.models import Team

class Organization(models.Model):
	name = models.CharField(max_length=32)
	date_created = models.DateTimeField(auto_now_add=True)
	members = models.ManyToManyField(User)
	teams = models.ManyToManyField(Team)

	def __str__(self):
		return self.name
