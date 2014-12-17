#encoding: utf8
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import json

from aeSupernova.encoder.Codification import Codification
from aeSupernova.header.Header import Header
from login.models import Log
from login.views import get_time
from pulsarInterface.Offer import Offer
from pulsarInterface.OpticalSheet import OpticalSheet
from pulsarInterface.TimePeriod import TimePeriod


MAX_NUMBER_OF_CODES = 100  # Not possible to add more codes after 99 

@login_required
def openSite(request):
    header = Header()
    header.setTimePeriodFunction('start()')
    header.setTermFunction('showPossibleOffers($("#headerCycle").val(),$("#headerTerm").val())')
    return render_to_response('encoder.html',{'header':header.getHtml()},context_instance=RequestContext(request))

def possibleCodifications(request):
    data = request.GET
    opticalSheets = OpticalSheet.find(timePeriod = TimePeriod.pickById(data['idTimePeriod']))
    encodedOpticalSheets = [opticalSheet for opticalSheet in opticalSheets if opticalSheet.encodingName != None]
    opticalSheet_dict = []
    for opticalSheet in encodedOpticalSheets:
        opticalSheet_dict.append({'idOpticalSheet':opticalSheet.idOpticalSheet, 'encodingName':opticalSheet.encodingName})
    return HttpResponse(json.dumps(opticalSheet_dict))

def offers_to_dict(offers):
    offers_dict = []
    for offer in offers:
        courseFound = False
        for course_dict in offers_dict:
            if course_dict['idCourse'] == offer.course.idCourse:
                course_dict['offers'].append({'idOffer':offer.idOffer, 'professorName':offer.professor.name, 'classNumber':offer.classNumber})
                courseFound = True
        if not courseFound:
            course = offer.course
            offers_dict.append({'idCourse':course.idCourse, 'courseName':course.name, 'courseCode':course.courseCode, 'offers':[{'idOffer':offer.idOffer, 'professorName':offer.professor.name, 'classNumber':offer.classNumber}]})
    return offers_dict
    
def fillOffers(request):
    data = request.GET
    codification = Codification.update(int(data['idOpticalSheet']), int(data['idTimePeriod']))
    if isinstance(codification, (str, unicode)):
        return HttpResponse(json.dumps(offers_to_dict(codification)))
    codification.fillOffers()
    return HttpResponse(json.dumps(offers_to_dict(codification.offers)))
    
def deleteEncoding(request):
    data = request.GET
    opticalSheet = OpticalSheet.pickById(int(data['idOpticalSheet']))
    user= request.user
    user_name = request.user.username
    time = get_time()
    timePeriod = str(TimePeriod.pickById(int(data['idTimePeriod'])))
    action = u"Usuário " + str(user_name) + u" deletou codificação " + opticalSheet.encodingName \
    + u" { Periodo: " + timePeriod + " }"
    encoding_delete_log = Log(user=user, action=action, time=time)
    encoding_delete_log.save()
    opticalSheet.delete()
    return HttpResponseRedirect('/encoder/')
    
def setOffers(request):
    data = request.GET
    data = json.loads(data['json'])
    codification = Codification.update(int(data['idOpticalSheet']), int(data['idTimePeriod']))
    if isinstance(codification, (str, unicode)):
        return HttpResponse(json.dumps(offers_to_dict(codification)))
    offers = []
    for idOffer in data['idOffers']:
        offers.append(Offer.pickById(int(idOffer)))
    if len(offers) > MAX_NUMBER_OF_CODES:
        return HttpResponse(json.dumps("It's over one hundred!"))
    codification.setOffers(offers)
    codification.store()
    return HttpResponse(json.dumps('OK'))
    
def newEncoding(request):
    data = request.GET
    codification = Codification.new(data['name'], int(data['idTimePeriod']))
    return HttpResponse(json.dumps(codification.os.idOpticalSheet))
    
def showPossibleOffers(request):
    data = request.GET
    codification = Codification.update(int(data['idOpticalSheet']), int(data['idTimePeriod']))
    if isinstance(codification, (str, unicode)):
        return HttpResponse(json.dumps(offers_to_dict(codification)))
    codification.fillPossibleOffers(int(data['idCycle']), int(data['term']))
    return HttpResponse(json.dumps(offers_to_dict(codification.possibleOffers)))
