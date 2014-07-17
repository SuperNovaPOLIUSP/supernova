from django import http
from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def index(request):
    if request.user.is_authenticated():    
        return render_to_response('index.html')
    else:
        return HttpResponseRedirect('/login/')

