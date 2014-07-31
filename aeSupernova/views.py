from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

def index(request):
    if request.user.is_authenticated():    
        return render_to_response('index.html')
    else:
        return HttpResponseRedirect('/login/')

