from django.db import models

from users.models import User

class Team(models.Model):
	name = models.CharField(max_length=32, unique=True)
	date_created = models.DateTimeField(auto_now_add=True)
	members = models.ManyToManyField(User, related_name='teams')

	def __str__(self):
		return self.name
