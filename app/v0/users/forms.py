from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	email = forms.CharField(required=False)

	class Meta:
		model = User
		fields = ('username', 'password', 'first_name', 'last_name', 'email')

class LoginForm(AuthenticationForm):
	# See https://docs.djangoproject.com/en/1.10/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm
	pass
