from django.shortcuts import render_to_response
from django.template import RequestContext
from django import http
from django.http import *

def index(request):
    return render_to_response('index.html')

