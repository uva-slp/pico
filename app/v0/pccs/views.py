from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import generic

import os
from subprocess import Popen, PIPE

def index(request):
    return HttpResponse('Hello world! How are you?')

def github_hook(request):
	if os.path.isfile('/home/slp/pccs/html/github-hook.php'):
		p = Popen(['php','/home/slp/pccs/html/github-hook.php'], stderr=PIPE)
		output, errors = p.communicate()
		if not p.returncode and not errors:
			return HttpResponse('Success!')
		return HttpResponseServerError('Failed to pull from git repo.')
	return HttpResponseNotFound('Unable to find github hook script.')
