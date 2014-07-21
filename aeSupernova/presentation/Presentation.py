# -*- coding: utf-8 -*-
#Embedded file name: /home/www/aeSupernova/aeSupernova/presentation/Presentation.py
from django.template.loader import *
from django.http import *

from pulsarInterface.IdealTermCourse import *
from pulsarInterface.Faculty import *
from pulsarInterface.Cycle import *
from pulsarInterface.TimePeriod import *

class Presentation(object):

    @staticmethod
    def findReports(idTimePeriod, idFaculty, idCycle, term):
        
        reports = []
        
        if idTimePeriod != 0 and idFaculty !=0 and idCycle !=0:
            timePeriod = TimePeriod.pickById(idTimePeriod)
            cycle = Cycle.pickById(idCycle)
            faculty = Faculty.pickById(idFaculty)
            idealTermCourses = IdealTermCourse.find(idCycle = idCycle)
            index = 0
            print len(idealTermCourses)
            while(index < len(idealTermCourses)):
                print idealTermCourses[index].term
                if idealTermCourses[index].term != term:
                    item = idealTermCourses[index]
                    idealTermCourses.remove(item)
                    index -= 1
                index += 1
            for iTC in idealTermCourses:
                reports.append({'year': {'name':timePeriod.year, 'id':timePeriod.year},
                 'session':{'name':timePeriod.session, 'id':timePeriod.session},
                 'faculty':{'name':faculty.name, 'id': idFaculty},
                 'cycle':{'name':cycle.name, 'id':idCycle},
                 'term':{'name':iTC.term, 'id':iTC.term},
                 'course':{'name':iTC.course.name, 'id':iTC.course.idCourse}})
        return reports
        #reports = apresentacao2.findReports(idTimePeriod, idFaculty, idCycle, term)

    @staticmethod
    def getReport(data):
        path = settings.MEDIA_ROOT + 'relatorios/disciplinas/'
        folder = str(data['course']['id']) + '/'
        course = Course.pickById(int(data['course']['id']))
        reportName = 'cde' + str(data['year']['name']) + 's' + str(data['session']['name']) + course.courseCode.lower() + '.pdf'
        pdf = file(path + folder + reportName).read()
        response = HttpResponse(pdf)
        response['Content-Type'] = 'application/pdf'
        response['Content-disposition'] = 'attachment; filename=' + reportName
        return response
