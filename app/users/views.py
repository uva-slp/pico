from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from common.decorators import anonymous_required
from .forms import UserForm, LoginForm

@anonymous_required
def register(request):
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			auth_login(request, user)

			return redirect(reverse('home'))
	else:
		user_form = UserForm()

	return render(
		request,
		'users/register.html',
		{'user_form': user_form})

@anonymous_required
def login(request):
	if request.method == 'POST':
		login_form = LoginForm(data=request.POST)

		if login_form.is_valid():
			auth_login(request, login_form.user_cache)
			return redirect(reverse('home'))

	else:
		login_form = LoginForm()

	return render(
		request,
		'users/login.html',
		{'login_form': login_form})

def logout(request):
	if request.user.is_authenticated():
		auth_logout(request)
	return redirect(reverse('index'))

@login_required
def password_change(request):
	if request.method == 'POST':
		password_change_form = PasswordChangeForm(request.user, data=request.POST)

		if password_change_form.is_valid():
			password_change_form.save()
			update_session_auth_hash(request, password_change_form.user)
			return redirect(reverse('home'))

	else:
		password_change_form = PasswordChangeForm(request.user)

	return render(
		request,
		'users/password_change.html',
		{'password_change_form': password_change_form})
