from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

from dal import autocomplete

from .models import User

class UserForm(UserCreationForm):
	username = forms.CharField(required=True)
	password2 = forms.CharField(label="Confirmation", widget=forms.PasswordInput,
		help_text="Enter the same password as above.")
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	email = forms.CharField(required=False)

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

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

class EmailValidationOnForgotPassword(PasswordResetForm):
	def clean_email(self):
		email = self.cleaned_data['email']
		if not User.objects.filter(email__iexact=email, is_active=True).exists():
			raise ValidationError("There is no user registered with the sepcified email address!")
		return email

