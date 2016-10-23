from django.db import models
from django.contrib.auth.models import User as AuthUser

class User(AuthUser):
	class Meta:
		proxy = True
		permissions = (
			('create_contest', 'Can create contests'),
		)

class Team(models.Model):
	name = models.CharField(max_length=32)
	date_created = models.DateTimeField(auto_now_add=True)
	members = models.ManyToManyField(User)
