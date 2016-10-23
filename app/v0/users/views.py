from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from common.decorators import anonymous_required

from users.forms import UserForm, LoginForm

@anonymous_required
def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			registered = True
	else:
		user_form = UserForm()

	return render(
		request,
		'users/register.html',
		{'user_form': user_form, 'registered': registered})

@anonymous_required
def login(request):
	if request.method == 'POST':
		login_form = LoginForm(data=request.POST)

		if login_form.is_valid():
			auth_login(request, login_form.user_cache)
			return redirect(reverse('contests:home'))

	else:
		login_form = LoginForm()

	return render(
		request,
		'users/login.html',
		{'login_form': login_form})

@login_required
def logout(request):
	auth_logout(request)
	return redirect(reverse('index'))
