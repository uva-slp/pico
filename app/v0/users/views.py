from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse

from users.forms import UserForm, LoginForm

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

def login(request):
	if request.method == 'POST':
		login_form = LoginForm(data=request.POST)

		user = authenticate(
			username=request.POST['username'],
			password=request.POST['password'])

		if user:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect(reverse('contests:home'))
			else:
				login_form.add_error(None, "Your account is disabled.")
		else:
			login_form.add_error(None, "Invalid username or password.")

	else:
		login_form = LoginForm()

	return render(
		request,
		'users/login.html',
		{'login_form': login_form})
