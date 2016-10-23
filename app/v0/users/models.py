from django.db import models
from django.contrib.auth.models import User as AuthUser, Group

class User(AuthUser):
	class Meta:
		proxy = True
		permissions = (
			('create_contest', 'Can create contests'),
		)

class Team(Group):
	class Meta:
		proxy = True
