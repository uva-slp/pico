from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import generic

import os
import subprocess

def index(request):
    return HttpResponse('Hello world!')

def github_hook(request):
	if os.path.isfile('/home/slp/pccs/html/github-hook.php'):
		output = subprocess.check_output('php /home/slp/pccs/html/github-hook.php', shell=True)
		return HttpResponse('Success!<br><br>%s'%(output))
	return HttpResponseNotFound('Unable to find github hook script.')
