from django.contrib.auth import backends
from .models import User

class ModelBackend(backends.ModelBackend):
	def get_user(self, user_id):
		'''
		Makes auth.User an instance of the proxy class
		'''
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
