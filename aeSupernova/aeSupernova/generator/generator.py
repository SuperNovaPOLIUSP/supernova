#coding: utf8
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
import json

from aeSupernova.generator.CourseGenerator import CourseReportGenerator
from aeSupernova.header.Header import Header
from login.models import Log
from login.views import get_time
from pulsarInterface.Course import Course
from pulsarInterface.Cycle import Cycle
from pulsarInterface.TimePeriod import TimePeriod
from tools.MySQLConnection import MySQLConnection


@login_required
def openSite(request):      
    header = Header()
    header.setTermFunction('loadCourses($("#headerTimePeriod").val(),$("#headerCycle").val(),$("#headerTerm").val())')
    return render_to_response('generator.html',{'header':header.getHtml()})


def loadCourses(request):
    data = request.GET
    cursor = MySQLConnection()
    coursesData = cursor.execute('SELECT course.idCourse, course.name, course.courseCode FROM rel_cycle_opticalSheet JOIN aggr_opticalSheetField on aggr_opticalSheetField.idOpticalSheet = rel_cycle_opticalSheet.idOpticalSheet JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer JOIN course ON course.idCourse = aggr_offer.idCourse WHERE idTimePeriod = ' + str(data['idTimePeriod']) + ' AND idCycle = ' + str(data['idCycle']) + ' AND term = ' + str(data['term']) + ' GROUP BY idCourse')
    courses = [] 
    for courseData in coursesData:
        course = {}
        course['courseCode'] = courseData[2]
        course['name'] = courseData[1]
        course['idCourse'] = courseData[0]
        courses.append(course)
    assessmentsData = cursor.execute('SELECT aggr_survey.assessmentNumber FROM rel_cycle_opticalSheet JOIN aggr_opticalSheetField on aggr_opticalSheetField.idOpticalSheet = rel_cycle_opticalSheet.idOpticalSheet JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer JOIN aggr_survey ON aggr_survey.idOpticalSheet = rel_cycle_opticalSheet.idOpticalSheet WHERE idTimePeriod = ' + str(data['idTimePeriod']) + ' AND idCycle = ' + str(data['idCycle']) + ' AND term = ' + str(data['term']) + ' GROUP BY aggr_survey.assessmentNumber')
    assessments = [int(assessment[0]) for assessment in assessmentsData]
    response = {}
    response['courses'] = courses
    response['assessments'] = assessments
    return HttpResponse(json.dumps(response)) 

def generateCourses(request):
    data = request.GET
    idCourses = json.loads(data['idCourses']) #Do something with this list
    idCourses = [int(idCourse) for idCourse in idCourses]
    if int(data['useProfessorsName']) == 1:
        useProfessorsName = True
    else:
        useProfessorsName = False
    if int(data['byOffer']) == 1:
        byOffer = 1
    elif int(data['byOffer']) == 2:
        byOffer = 2
    elif int(data['byOffer']) == 0:
        byOffer = 0
    idTimePeriod = int(data['idTimePeriod'])
    idFaculty = int(data['idFaculty'])
    assessmentNumber = int(data['assessmentNumber'])
    user= request.user
    user_name = request.user.username
    time = get_time()
    timePeriod = str(TimePeriod.pickById(idTimePeriod))
    courses = [str(Course.pickById(idCourse).courseCode) for idCourse in idCourses]
    cycle = Cycle.pickById(int(data['idCycle'])).name
    action = u"Usuário " + str(user_name) + u" gerou relatório: " \
    + u"{ Curso: " + cycle \
    + u"; Semestre: " + data['term'] \
    + u"; Matérias: " + str(courses) \
    + u"; Período: " + timePeriod \
    + u"; Avaliação: " + data['assessmentNumber'] + " }"
    report_generate_log = Log(user=user, action=action, time=time)
    report_generate_log.save()
    CourseReportGenerator(idTimePeriod, idCourses, useProfessorsName, byOffer, idFaculty, assessmentNumber)
    return HttpResponse('Relatórios Gerados')
