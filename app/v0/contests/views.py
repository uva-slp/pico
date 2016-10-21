from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

def home(request):
	j = "foo"
	foo = "Make Travis run"
	please="please"
	please == please
	return HttpResponse('home page %s'%(please+foo+j))
