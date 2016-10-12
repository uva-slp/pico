from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import generic

import os
import subprocess
from subprocess import Popen, PIPE

def index(request):
    return HttpResponse('Hello world! How are you?')

def github_hook(request):
	if os.path.isfile('/home/slp/pccs/html/github-hook.php'):
		
		output = subprocess.check_output('php /home/slp/pccs/html/github-hook.php', shell=True)
		return HttpResponse('Success!<br><br>%s'%(output))

		# p = Popen(['php','/home/slp/pccs/html/github-hook.php'], stdout=PIPE, stderr=PIPE, env=os.environ)
		# output, errors = p.communicate()
		# if not p.returncode and not errors:
		# 	return HttpResponse('Success!')
		# return HttpResponseServerError('Failed to pull from git repo.<br><br>%s<br><br>%s'%(output, errors))
	
	return HttpResponseNotFound('Unable to find github hook script.')
