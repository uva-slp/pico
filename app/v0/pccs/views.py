from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import generic

from users.forms import LoginForm, UserForm

def index(request):
	return render(
		request,
		'pccs/index.html',
		{'login_form': LoginForm(), 'user_form': UserForm()})
