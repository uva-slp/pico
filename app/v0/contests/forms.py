from django.forms import Form, ModelForm
from .models import User, Contest
from django import forms

class CreateContestForm(ModelForm):
    class Meta:
        model = Contest
        fields = ['title']

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class LoginForm(Form):
    username = forms.CharField(label='username', max_length=16)
    password = forms.CharField(label='password', max_length=32, widget=forms.PasswordInput)
