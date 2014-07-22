from django import http
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from tools.MySQLConnection import *

from aeSupernova.header.Header import *

@login_required
def openSite(request):
    header = Header()
    header.setTermFunction('')
    header.setTimePeriodFunction('headerTermInit()')
    return render_to_response('control.html',{'header':header.getHtml()},context_instance=RequestContext(request))
 

def findData(request):
    data = request.GET
    cursor = MySQLConnection()
    wheres = []
    if data['idTimePeriod'] != '0':
        wheres.append('timePeriod.idTimePeriod = ' + data['idTimePeriod'])
    if data['idFaculty'] != '0':
        wheres.append('faculty.idFaculty = ' + data['idFaculty'])
    if data['idCycle'] != '0':
        wheres.append('cycle.idCycle = ' + data['idCycle'])
    if data['term'] != '0':
        wheres.append('rel_cycle_opticalSheet.term = ' + data['term'])
    whereQuery = ' AND '.join(wheres)
    print whereQuery

    datafilesData = cursor.execute('SELECT rel_cycle_opticalSheet.idOpticalSheet, rel_cycle_opticalSheet.idCycle, cycle.name, faculty.idFaculty, faculty.name, rel_cycle_opticalSheet.term, datafile.idDatafile, datafile.fileName, timePeriod.year, timePeriod.session FROM rel_cycle_opticalSheet JOIN aggr_opticalSheetField ON rel_cycle_opticalSheet.idOpticalSheet = aggr_opticalSheetField.idOpticalSheet JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer JOIN timePeriod ON timePeriod.idTimePeriod = aggr_offer.idTimePeriod JOIN cycle ON cycle.idCycle = rel_cycle_opticalSheet.idCycle JOIN rel_courseCoordination_cycle ON rel_courseCoordination_cycle.idCycle = cycle.idCycle JOIN rel_courseCoordination_faculty ON rel_courseCoordination_faculty.idCourseCoordination = rel_courseCoordination_cycle.idCourseCoordination JOIN faculty ON faculty.idFaculty = rel_courseCoordination_faculty.idFaculty JOIN rel_answer_opticalSheetField_survey ON rel_answer_opticalSheetField_survey.idOpticalSheetField = aggr_opticalSheetField.idOpticalSheetField JOIN answer ON answer.idAnswer = rel_answer_opticalSheetField_survey.idAnswer JOIN datafile ON datafile.idDatafile = answer.idDatafile WHERE ' + whereQuery + ' GROUP BY rel_cycle_opticalSheet.idOpticalSheet, rel_cycle_opticalSheet.idCycle, datafile.idDatafile')
    timePeriods = {}
    returnList = []
    for data in datafilesData:
        idDatafile = data[6]
        numberOfAnswers = len(cursor.execute('SELECT identifier FROM datafile JOIN answer ON answer.idDatafile = datafile.idDatafile WHERE datafile.idDatafile = ' + str(idDatafile) + ' GROUP BY datafile.idDatafile, identifier;'))
        returnDict = {}
        returnDict['opticalSheet'] = {'name': str(data[0]), 'id': data[0]}
        returnDict['cycle'] = {'name': data[2], 'id': data[1]}
        returnDict['faculty'] = {'name': data[4], 'id': data[3]}
        returnDict['term'] = {'name': data[5], 'id': data[5]}
        returnDict['year'] = {'name': data[8], 'id': data[8]}
        returnDict['session'] = {'name': data[9], 'id':data[9]}
        returnDict['datafile'] = {'name': data[7] , 'id':[6], 'numberOfAnswers':numberOfAnswers}
        returnList.append(returnDict)
    return HttpResponse(json.dumps(returnList)) 
        
