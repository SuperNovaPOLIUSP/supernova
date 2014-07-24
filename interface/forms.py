import autocomplete_light
from django import forms
from pulsarInterface.Course import Course
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
    
class OfferForm(forms.Form):
    timePeriods = TimePeriod.find()
    timePeriods.reverse()
    timePeriodNames = [str(timePeriod) for timePeriod in timePeriods]
    timePeriodIds = [t.idTimePeriod for t in timePeriods]
    timePeriodInfo = zip(timePeriodIds, timePeriodNames)
    dropDownTimePeriod = forms.ChoiceField(widget=forms.Select, choices=timePeriodInfo, label = '')
    inputCourse = forms.CharField(label = 'Codigo do Curso')
    
class OfferEditForm(forms.Form):
    courses = Course.find()
    courseCode = [course.courseCode for course in courses]
    courseIds = [course.idCourse for course in courses]
    courseInfo = zip(courseIds, courseCode)
    courseInfo = sorted(courseInfo, key=getKey)
    dropDownCourse = forms.ChoiceField(widget=forms.Select, choices=courseInfo, label = "")