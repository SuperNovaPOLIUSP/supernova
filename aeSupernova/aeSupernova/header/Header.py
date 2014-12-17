# coding: utf8
from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import *
import codecs
import json
from django.core import serializers
from django.template.loader import get_template
from django.template import Context

from tools.MySQLConnection import *
from pulsarInterface.TimePeriod import *
from pulsarInterface.Faculty import *



def possibleTerms(request):
    data = request.GET
    idCycle = int(data['idCycle'])
    timePeriod = TimePeriod.pickById(int(data['idTimePeriod']))
    print int(data['idTimePeriod'])
    cursor = MySQLConnection()
    if idCycle != 0 and timePeriod != None:
        possibleTerms = cursor.execute("SELECT rel_course_cycle.term FROM rel_course_cycle JOIN aggr_offer ON aggr_offer.idCourse = rel_course_cycle.idCourse WHERE idCycle = " + str(idCycle) + " AND aggr_offer.idTimePeriod = "  + str(timePeriod.idTimePeriod)  +  " AND rel_course_cycle.endDate = '0000-00-00' GROUP BY rel_course_cycle.term")
    elif idCycle != 0:
        possibleTerms = cursor.execute("SELECT rel_course_cycle.term FROM rel_course_cycle JOIN aggr_offer ON aggr_offer.idCourse = rel_course_cycle.idCourse WHERE idCycle = " + str(idCycle) + " AND rel_course_cycle.endDate = '0000-00-00' GROUP BY rel_course_cycle.term")
    elif timePeriod != None:
        possibleTerms = cursor.execute("SELECT rel_course_cycle.term FROM rel_course_cycle JOIN aggr_offer ON aggr_offer.idCourse = rel_course_cycle.idCourse WHERE aggr_offer.idTimePeriod = "  + str(timePeriod.idTimePeriod)  +  " AND rel_course_cycle.endDate = '0000-00-00' GROUP BY rel_course_cycle.term")
    else:
        possibleTerms = cursor.execute("SELECT rel_course_cycle.term FROM rel_course_cycle JOIN aggr_offer ON aggr_offer.idCourse = rel_course_cycle.idCourse WHERE rel_course_cycle.endDate = '0000-00-00' GROUP BY rel_course_cycle.term")
    if timePeriod != None:
        #Allow appearence of terms for new sessions (12 - second evaluation of first semester and 22 - second evaluation of second semester) 
        possibleTerms = [possibleTerm[0] for possibleTerm in possibleTerms if possibleTerm[0]%2 == timePeriod.session%2 or timePeriod.length == 2 or timePeriod.session == 12 or timePeriod.session == 22]
    else:
        possibleTerms = [possibleTerm[0] for possibleTerm in possibleTerms]
    return HttpResponse(json.dumps(possibleTerms))

class HeaderError(Exception):
    """
     Exception reporting an error in the execution of a Header method.

    :version:
    :author:
    """
    pass

class Header(object):
    def __init__(self):
        #coloca as funcoes padroes para o cabecalho
        self.timePeriodFunction = 'headerFacultyInit()'
        self.facultyFunction = 'headerCycleInit()'
        self.cycleFunction = 'headerTermInit()'
        self.termFunction = ''

    def setTimePeriodFunction(self, timePeriodFunction):
        if not isinstance(timePeriodFunction, (str, unicode)):
            raise HeaderError('timePeriodFunction parameter must be a string or an unicode.')
        self.timePeriodFunction = timePeriodFunction

    def setFacultyFunction(self, facultyFunction):
        if not isinstance(facultyFunction, (str, unicode)):
            raise HeaderError('facultyFunction parameter must be a string or an unicode.')
        self.facultyFunction = facultyFunction

    def setCycleFunction(self, cycleFunction):
        if not isinstance(cycleFunction, (str, unicode)):
            raise HeaderError('cycleFunction parameter must be a string or an unicode.')
        self.cycleFunction = cycleFunction

    def setTermFunction(self, termFunction):
        if not isinstance(termFunction, (str, unicode)):
            raise HeaderError('termFunction parameter must be a string or an unicode.')
        self.termFunction = termFunction

    def getHtml(self):
        timePeriods = TimePeriod.find()
        timePeriodsList = []
        for timePeriod in timePeriods:
            timePeriodDict = {}
            timePeriodDict['text'] = str(timePeriod)
            timePeriodDict['idTimePeriod'] = timePeriod.idTimePeriod
            timePeriodsList.insert(0,timePeriodDict) #To get them in the right order
        faculties = Faculty.find()
        facultiesList = []
        cyclesList = []
        for faculty in faculties:
            if len(faculty.courseCoordinations) > 0:
                facultyDict = {}
                facultyDict['name'] = faculty.name
                facultyDict['idFaculty'] = faculty.idFaculty
                facultiesList.append(facultyDict)
                for courseCoordination in faculty.courseCoordinations:
                    for cycle in courseCoordination.cycles:
                        cycleDict = {}
                        cycleDict['name'] = cycle.name
                        cycleDict['idCycle'] = cycle.idCycle
                        cycleDict['idFaculty'] = faculty.idFaculty
                        cycleDict['dayPeriod'] = cycle.dayPeriod
                        cyclesList.append(cycleDict)
        finalDict = {}
        finalDict['timePeriodsList'] = timePeriodsList
        finalDict['facultiesList'] = facultiesList
        finalDict['cyclesList'] = cyclesList
        finalDict['timePeriodFunction'] = self.timePeriodFunction
        finalDict['facultyFunction'] = self.facultyFunction
        finalDict['cycleFunction'] = self.cycleFunction
        finalDict['termFunction'] = self.termFunction

        t = get_template('header.html')
        return t.render(Context(finalDict))
        

