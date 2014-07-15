#Embedded file name: /home/www/aeSupernova/aeSupernova/presentation/presentation.py
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from django import http
from django.http import *
from aeSupernova.header.Header import *
from aeSupernova.presentation.Presentation import *

def openSite(request):
    header = Header()
    header.setTermFunction('')
    header.setTimePeriodFunction('headerTermInit()')
    return render_to_response('presentation.html', {'header': header.getHtml()}, context_instance=RequestContext(request))


def findReports(request):
    data = request.GET
    response = Presentation.findReports(int(data['idTimePeriod']), int(data['idFaculty']), int(data['idCycle']), int(data['term']))
    return HttpResponse(json.dumps(response))


def getReport(request):
    data = request.GET
    data = json.loads(data['json'])
    return Presentation.getReport(data)
