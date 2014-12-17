#encoding: utf8

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import json

from aeSupernova.header.Header import Header
from aeSupernova.opticalSheet.ColumnsController import ColumnsController
from aeSupernova.opticalSheet.OpticalSheetController import \
    OpticalSheetController
from aeSupernova.opticalSheet.OpticalSheetPrinter import OpticalSheetPrinter
from aeSupernova.opticalSheet.QualitativeQuestionnairePrinter import \
    QualitativeQuestionnairePrinter
from aeSupernova.opticalSheet.QuestionController import QuestionController
from login.models import Log
from login.views import get_time
from pulsarInterface.Cycle import Cycle
from pulsarInterface.TimePeriod import TimePeriod


@login_required
def openSite(request):
    header = Header()
    header.setTermFunction('loadOpticalSheet($("#headerTimePeriod").val(),$("#headerCycle").val(),$("#headerTerm").val())')
    return render_to_response('folha2.html',{'header':header.getHtml()},context_instance=RequestContext(request))

def findCourses(request):
    data = request.GET
    response = ColumnsController.findCourses(data['abbreviation'], data['courseCode'], '', int(data['idTimePeriod']), int(data['idCycle']), int(data['term']))
    return HttpResponse(json.dumps(response))

def getCourses(request):
    data = request.GET
    response = ColumnsController.findCourses('', '', '', int(data['idTimePeriod']), int(data['idCycle']), int(data['term']))
    return HttpResponse(json.dumps(response))

def expandCourse(request):
    data = request.GET
    response = ColumnsController.expandCourse(int(data['idCourse']), int(data['idTimePeriod']))
    return HttpResponse(json.dumps(response))

def findOffers(request):
    data = request.GET
    response = ColumnsController.getOffers(data['courseCode'], int(data['idTimePeriod']))
    return HttpResponse(json.dumps(response))

def getAnswerTypes(request):
    response = QuestionController.getAnswerTypes()
    return HttpResponse(json.dumps(response))

def getQuestions(request):
    response = QuestionController.findQuestion('')
    return HttpResponse(json.dumps(response))

def storeQuestions(request):
    data = request.GET
    response = QuestionController.storeQuestion(data['idAnswerType'], data['questionWording'])
    return HttpResponse(json.dumps(response))


def findOpticalSheetByTimePeriod_Cycle_Term(request):
    data = request.GET
    response = OpticalSheetController.findOpticalSheetByTimePeriod_Cycle_Term(int(data['idTimePeriod']), int(data['idCycle']), int(data['term']))
    return HttpResponse(json.dumps(response))

def findOpticalSheetById(request):
    data = request.GET
    response = OpticalSheetController.findOpticalSheetById(int(data['idOpticalSheet']))
    return HttpResponse(json.dumps(response))

def store(request):
    data = request.POST
    data = json.loads(data['json'])
    user= request.user
    user_name = request.user.username
    time = get_time()
    cycle_name = Cycle.pickById(int(data['idCycle'])).name
    timePeriod = str(TimePeriod.pickById(int(data['idTimePeriod'])))
    response = OpticalSheetController.storeOpticalSheet(data['idOpticalSheet'], data['surveyType'], data['idCycle'], data['term'], data['idTimePeriod'], data['fields'], data['surveys'], data['encoded'])
    action = u"Usuário " + str(user_name) + u" salvou idOpticalSheet " + str(data['idOpticalSheet']) \
    + u" { Periodo: " + timePeriod \
    + u"; Curso: " + cycle_name \
    + u"; Semestre: " + str(data['term']) + " }"
    opticalSheet_store_log = Log(user=user, action=action, time=time)
    opticalSheet_store_log.save()
    return HttpResponse(json.dumps(response))

def printOpticalSheet(request):
    data = request.POST
    jsonString = data['json']
    data = json.loads(jsonString)
    opticalSheetPrinter = OpticalSheetPrinter(data['idCycle'], data['term'], data['idTimePeriod'])
    opticalSheetPrinter.printOpticalSheet(data['idOpticalSheet'], data['fields'], data['survey'], data['positions'])
    return HttpResponse('ok')

def printAMC(request):
    data = request.POST
    jsonString = data['json']
    data = json.loads(jsonString)
    opticalSheetPrinter = OpticalSheetPrinter(data['idCycle'], data['term'], data['idTimePeriod'])
    opticalSheetPrinter.printAMC(data['idOpticalSheet'], data['fields'], data['survey'], data['positions'])
    return HttpResponse('ok')

def getPrintedOpticalSheet(request):
    data = request.GET
    opticalSheetPrinter = OpticalSheetPrinter(int(data['idCycle']), int(data['term']), int(data['idTimePeriod']))
    if data['downloadType'] == 'pdf':
        return opticalSheetPrinter.getPDF()
    elif data['downloadType'] == 'tex':
        return opticalSheetPrinter.getTex()
    
def getPrintedAMC(request):
    data = request.GET
    opticalSheetPrinter = OpticalSheetPrinter(int(data['idCycle']), int(data['term']), int(data['idTimePeriod']))
    if data['downloadType'] == 'pdf':
        return opticalSheetPrinter.getPDF()
    elif data['downloadType'] == 'tex':
        return opticalSheetPrinter.getTex()

def printQualitativeQuestionnaire(request):
    data = request.POST
    data = json.loads(data['json'])
    qqPrinter = QualitativeQuestionnairePrinter( int(data['idTimePeriod']), int(data['idCycle']), int(data['term']))
    qqPrinter.printQualitativeQuestionnaire(int(data['idOpticalSheet']), int(data['numberOfAnswerLines']), int(data['qualitativeQuestionnaireType']))
    return HttpResponse('ok')

def getPrintedQualitativeQuestionnaire(request):
    data = request.GET
    qqPrinter = QualitativeQuestionnairePrinter( int(data['idTimePeriod']), int(data['idCycle']), int(data['term']))
    if data['downloadType'] == 'pdf':
        return qqPrinter.getPDF()
    elif data['downloadType'] == 'tex':
        return qqPrinter.getTex()

def getEncodings(request):
    data = request.GET
    response = ColumnsController.getEncodings(data['idTimePeriod'])
    return HttpResponse(json.dumps(response))

def removeCycleFromOpticalSheet(request):
    data = request.GET
    ColumnsController.removeCycleFromOpticalSheet(data['idCycle'], data['term'], data['idOpticalSheet'])
    return HttpResponse('')

def listOldOpticalSheets(request):
    data = request.GET
    response = OpticalSheetController.getOldOpticalSheets(data['idCycle'])
    return HttpResponse(json.dumps(response))

