from django import forms
from django.db import models
from django.contrib.auth.models import User, Group

class UserForm(forms.ModelForm):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	email = forms.CharField(required=False)

	class Meta:
		model = User
		fields = ('username', 'password', 'first_name', 'last_name', 'email')

class LoginForm(forms.ModelForm):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True)
	
	class Meta:
		model = User
		fields = ('username', 'password')
