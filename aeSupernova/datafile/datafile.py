#coding: utf8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from login.models import Log
from login.views import get_time
from pulsarInterface.Cycle import Cycle
from pulsarInterface.TimePeriod import TimePeriod

from aeSupernova.datafile.NoteReader import NoteReader
from aeSupernova.header.Header import Header


@login_required
def openSite(request):
    header = Header()
    header.setTermFunction('$("#file").show()')
    if request.method == 'POST':
        data = request.POST
        NoteReader.readNote(request.FILES['arq'].name, request.FILES['arq'].file.getvalue(),int(data['headerCycle']), int(data['headerTerm']), int(data['headerTimePeriod']), int(data['bSheet']), int(data['assessmentNumber']))
        user= request.user
        user_name = request.user.username
        time = get_time()
        cycle_name = Cycle.pickById(int(data['headerCycle'])).name
        timePeriod = str(TimePeriod.pickById(int(data['headerTimePeriod'])))
        b_sheet = "A" if int(data['bSheet']) == 0 else "B"
        action = u"Usuário " + str(user_name) + " inseriu datafile " + request.FILES['arq'].name \
        + u" { Curso: " + cycle_name \
        + u"; Semestre: " + data['headerTerm'] \
        + u"; Período: " + timePeriod \
        + u"; Folha(A ou B): " + b_sheet \
        + u"; Avaliação: " + data['assessmentNumber'] + " }"
        datafile_insert_log = Log(user=user, action=action, time=time)
        datafile_insert_log.save()
    return render_to_response('datafile.html',{'divs':header.getHtml()},context_instance=RequestContext(request))    

