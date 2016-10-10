from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import generic

import subprocess
import os

def index(request):
    return HttpResponse('Hello world!')

def github_hook(request):
	if os.path.isfile('/home/slp/pccs/html/github-hook.php'):
		subprocess.call('/usr/bin/php /home/slp/pccs/html/github-hook.php')
		return HttpResponse('Success!')
	raise Http404
