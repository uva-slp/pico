from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import generic

from common.decorators import anonymous_required
from users.forms import LoginForm, UserForm

@anonymous_required
def index(request):
	return render(
		request,
		'pccs/index.html',
		{'login_form': LoginForm(), 'user_form': UserForm()})
