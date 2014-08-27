from django import http
from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def index(request):
    if request.user.is_authenticated():    
        return render_to_response('index.html')
    else:
        return HttpResponseRedirect('/login/')

def initial(request):
	return render_to_response('initial.html')

def historico(request):
	return render_to_response('historico.html')

def equipe(request):
	return render_to_response('equipe.html')

def ideia(request):
	return render_to_response('ideia.html')

def fotos(request):
	return render_to_response('fotos.html')

def relatoriosgerais(request):
	return render_to_response('relatoriosgerais.html')

def outrasaplicacoes(request):
	return render_to_response('outrasaplicacoes.html')

def publicacoes(request):
	return render_to_response('publicacoes.html')

def parcerias(request):
	return render_to_response('parcerias.html')

def embreve(request):
	return render_to_response('embreve.html')

