from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required

from common.decorators import anonymous_required
from contests.models import Contest
from users.forms import LoginForm, UserForm

@anonymous_required
def index(request):
	return render(
		request,
		'pccs/index.html',
		{'login_form': LoginForm(), 'user_form': UserForm()})

@login_required
def home(request):
	return render(
		request,
		'pccs/home.html',
		{
			'active_contests': Contest.objects.active(),
		}
	)
