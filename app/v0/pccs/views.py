from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

def index(request):
    return HttpResponse('Hello world!')
