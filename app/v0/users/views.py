from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login

from users.forms import UserForm

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
			print(user_form.errors)
	else:
		user_form = UserForm()

	context = {

	}

	return render(
		request,
		'users/register.html',
		{'user_form': user_form, 'registered': registered})

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect('/contests/home')
			else:
				return HttpResponse("Your account is disabled.")
		else:
			return HttpResponse("Invalid login details supplied.")

	else:
		return render(request, 'users/login.html', {})
