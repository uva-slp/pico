from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

from dal import autocomplete

from .models import User

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

class UserSelectForm(forms.ModelForm):
	user = forms.ModelChoiceField(queryset=User.objects.all())

	class Meta:
		model = User
		fields = ('user',)

class UserSearchForm(forms.ModelForm):
	user = forms.ModelChoiceField(queryset=User.objects.all(),
		widget=autocomplete.ModelSelect2(
			url=reverse_lazy('users:autocomplete'),
			attrs={
				'data-placeholder': 'User',
			})
	)

	class Meta:
		model = User
		fields = ('user',)
