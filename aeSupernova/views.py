from django.http.response import HttpResponseRedirect
from django.shortcuts import render

def index(request):
    if request.user.is_authenticated():    
        return render(request, 'index.html')
    else:
        return HttpResponseRedirect('/login/')

