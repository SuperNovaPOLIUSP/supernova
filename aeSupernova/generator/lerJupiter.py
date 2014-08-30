from django.http.response import HttpResponse
from django.shortcuts import render_to_response
import json

from aeSupernova.header.Header import Header


def openSite(request):
    header = Header()
    header.setFacultyFunction('findCycles($("#headerFaculty").val())')
    return render_to_response('lerJupiter.html',{'header':header.getHtml()})

def lerJupiter(request):
    data = request.GET
    idCycles = json.loads(data['idCycles']) #Do something with this list
    idCycles = [int(idCycle) for idCycle in idCycles]
    return HttpResponse('ok')
