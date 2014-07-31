# -*- coding: utf-8 -*-
from django import forms
from pulsarInterface.Course import Course
from pulsarInterface.Professor import Professor
from pulsarInterface.Cycle import Cycle
from pulsarInterface.TimePeriod import TimePeriod
from pulsarInterface.IdealTermCourse import IdealTermCourse
from pulsarInterface.Schedule import Schedule
import datetime

def getKey(item):
    return item[1]


class ProfessorForm(forms.Form):
    name = forms.CharField(max_length = 255, required = True, label = 'Name')
    memberId = forms.IntegerField(required = True, label = 'Member ID')
    office = forms.CharField(max_length = 45, required = False, label = 'Office')
    email = forms.CharField(max_length = 65, required = False, label = 'Email')
    phoneNumber = forms.IntegerField(required = False, label = 'Phone Number')
    cellphoneNumber = forms.IntegerField(required = False, label = 'CellPhone Number')
    idDepartment = forms.IntegerField(required = False, label = 'ID Department')

class IndexForm(forms.Form):
    def updateForm(self):
        timePeriods = TimePeriod.find()
        timePeriods.reverse()
        timePeriodNames = [str(timePeriod) for timePeriod in timePeriods]
        timePeriodIds = [t.idTimePeriod for t in timePeriods]
        timePeriodInfo = zip(timePeriodIds, timePeriodNames)
        courses = Course.find()
        courseCode = [course.courseCode for course in courses]
        courseIds = [course.idCourse for course in courses]
        courseInfo = zip(courseIds, courseCode)
        courseInfo = sorted(courseInfo, key=getKey)
        self.fields['dropDownTimePeriod'] = forms.ChoiceField(widget=forms.Select, choices=timePeriodInfo, label = 'Periodo')
        self.fields['dropDownCourse'] = forms.ChoiceField(widget=forms.Select, choices=courseInfo, label = 'Codigo do Curso')

class OfferForm(forms.Form):
    classNumber = forms.IntegerField(required = True, label = 'Número da Turma')
    teoricaPraticaInfo = [[0,'Teórica'],[1,'Prática']]
    dropDownTeoricaPratica = forms.ChoiceField(widget=forms.Select, choices=teoricaPraticaInfo, label = "TEÓRICA/PRÁTICA")
    numberOfRegistrations = forms.IntegerField(required = False, label = 'Número de Matriculados')

    def updateForm(self):
        professors = Professor.find()
        professorName = [professor.name for professor in professors]
        professorIds = [professor.idProfessor for professor in professors]
        professorInfo = zip(professorIds, professorName)
        professorInfo = sorted(professorInfo, key=getKey)
        schedules = Schedule.find()
        scheduleName = schedules
        scheduleIds = [schedule.idSchedule for schedule in schedules]
        scheduleInfo = zip(scheduleIds, scheduleName)
        self.fields['dropDownProfessor'] = forms.ChoiceField(widget=forms.Select, choices=professorInfo, label = "Professor")
        self.fields['listSchedules'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=scheduleInfo, label = 'Horários')



class CrawlerForm(forms.Form):
    cycles = Cycle.find()
    timePeriods = TimePeriod.find(year=datetime.datetime.now().year)
    for cycle in cycles:
        cycle.completeMandatoryIdealTerms()
    cycleTuple = ((cycle.idCycle, cycle.name + ' - ' + cycle.dayPeriod + ' - id: ' + str(cycle.idCycle)) for cycle in cycles if len(cycle.mandatoryIdealTerms))
    timePeriodTuple = ((timePeriod.idTimePeriod, str(timePeriod)) for timePeriod in timePeriods)
    cycle = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=cycleTuple, label='Ciclo')
    timePeriod = forms.ChoiceField(choices=timePeriodTuple, label='Período')


def offer_to_string(offer):
    string = ''
    string += offer.course.name
    string += ' - '
    string += offer.course.courseCode
    string += '\n'
    string += offer.professor.name
    string += '\nTurma: '
    string += str(offer.classNumber)
    string += '\n'
    for schedule in offer.schedules:
        string += str(schedule).decode('utf-8')
        string += '\n'
    return string


class CrawlerResultsForm(forms.Form):
    offers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def update_offers(self, offers):
        ids_offer = (offer for offer in offers)
        text_offer = (offer_to_string(offer) for offer in offers)
        offer_information = zip(ids_offer, text_offer)
        self.fields['offers'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=offer_information)
