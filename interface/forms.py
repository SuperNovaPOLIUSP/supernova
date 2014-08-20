#coding: utf8
from django import forms

from pulsarInterface.Course import Course
from pulsarInterface.Cycle import Cycle
from pulsarInterface.Professor import Professor
from pulsarInterface.Schedule import Schedule
from pulsarInterface.TimePeriod import TimePeriod


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

class OfferListForm(forms.Form):
    def updateForm(self):
        timePeriods = TimePeriod.find()
        timePeriods.reverse()
        timePeriodNames = [str(timePeriod) for timePeriod in timePeriods]
        timePeriodIds = [t.idTimePeriod for t in timePeriods]
        timePeriodInfo = zip(timePeriodIds, timePeriodNames)
        cycles = Cycle.find()
        cycleName = [cycle.name for cycle in cycles]
        cycleIds = [cycle.idCycle for cycle in cycles]
        cycleInfo = zip(cycleIds, cycleName)
        termInfo = [[0,"Todos"],[1,'1º Semestre'],[2,'2º Semestre'],[3,'3º Semestre'],[4,'4º Semestre'],[5,'5º Semestre'],[6,'6º Semestre'],[7,'7º Semestre'],[8,'8º Semestre'],[9,'9º Semestre'],[10,'10º Semestre']]
        self.fields['dropDownCycle'] = forms.ChoiceField(widget=forms.Select, choices=cycleInfo, label = 'Curso')
        self.fields['dropDownTimePeriod'] = forms.ChoiceField(widget=forms.Select, choices=timePeriodInfo, label = 'Periodo')
        self.fields['dropDownTerm'] = forms.ChoiceField(widget=forms.Select, choices=termInfo, label = 'Semestre')
        