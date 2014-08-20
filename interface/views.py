#coding: utf8
import commands
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.context import Context
from django.template.loader import render_to_string
import io

from interface.forms import ProfessorForm, IndexForm, OfferForm, OfferListForm
from pulsarInterface.Course import Course
from pulsarInterface.CourseCoordination import CourseCoordination
from pulsarInterface.Cycle import Cycle
from pulsarInterface.Department import Department
from pulsarInterface.Faculty import Faculty
from pulsarInterface.IdealTermCourse import IdealTermCourse
from pulsarInterface.Offer import Offer
from pulsarInterface.Professor import Professor
from pulsarInterface.Schedule import Schedule
from pulsarInterface.TimePeriod import TimePeriod


@login_required
def index(request):
    form = IndexForm()
    form.updateForm()
    rendered_page = render(request, 'interface_index.html', {'form': form})
    return rendered_page

@login_required
def professor(request):
    professors = Professor.find()
    rendered_page = render(request, 'professor.html', {'professors': professors})
    return rendered_page

@login_required
def professor_detail(request, idProfessor):
    professor = Professor.pickById(idProfessor)
    rendered_page = render(request, 'professor_detail.html', {'professor': professor})
    return rendered_page

@login_required
def professor_edit(request, idProfessor):
    professor = Professor.pickById(idProfessor)
    if request.method  == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            memberId = form.cleaned_data['memberId']
            office = form.cleaned_data['office']
            email = form.cleaned_data['email']
            phoneNumber = form.cleaned_data['phoneNumber']
            cellphoneNumber = form.cleaned_data['cellphoneNumber']
            idDepartment = form.cleaned_data['idDepartment']
            professor.name = name
            professor.memberId = memberId
            office = None if not office else office
            email = None if not email else email
            professor.office = office
            professor.email = email
            professor.phoneNumber = phoneNumber
            professor.cellphoneNumber = cellphoneNumber
            professor.idDepartment = idDepartment
            professor.store()
            return HttpResponseRedirect('/interface/professor/' + str(idProfessor))
    else:
        form = ProfessorForm(initial={'name': professor.name, 
                                      'idDepartment': professor.idDepartment, 
                                      'memberId': professor.memberId, 
                                      'office': professor.office, 
                                      'email': professor.email, 
                                      'phoneNumber': professor.phoneNumber,
                                      'cellphoneNumber': professor.cellphoneNumber})
    rendered_page = render(request, 'professor_edit.html', {'professor': professor, 'form': form})
    return rendered_page

@login_required
def professor_delete(request, idProfessor):
    professor = Professor.pickById(idProfessor)
    professor.delete()
    return HttpResponseRedirect('/interface/professor/') 

@login_required
def professor_create(request):
    if request.method  == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            memberId = form.cleaned_data['memberId']
            office = form.cleaned_data['office']
            email = form.cleaned_data['email']
            phoneNumber = form.cleaned_data['phoneNumber']
            cellphoneNumber = form.cleaned_data['cellphoneNumber']
            idDepartment = form.cleaned_data['idDepartment']
            professor = Professor(name)
            professor.setMemberId(memberId)
            if office:
                professor.setOffice(office)
            if email:
                professor.setEmail(email)
            if phoneNumber:
                professor.setPhoneNumber(phoneNumber)
            if cellphoneNumber:
                professor.setCellphoneNumber(cellphoneNumber)
            if idDepartment:
                professor.setDepartment(Department.pickById(idDepartment))
            professor.store()
            return HttpResponseRedirect('/interface/professor/' + str(professor.idProfessor))
    else:
        form = ProfessorForm()
    rendered_page = render(request, 'professor_create.html', {'form': form})
    return rendered_page

@login_required
def offer(request):
    if request.method  == 'POST':
        form = IndexForm(request.POST)
        form.updateForm()
        if form.is_valid():
            timePeriod = TimePeriod.pickById(form.cleaned_data['dropDownTimePeriod'])
            course = Course.pickById(form.cleaned_data['dropDownCourse'])
            offers = Offer.find(timePeriod=timePeriod, course=course)
            rendered_page = render(request, 'offer.html', {'offers': offers, 'timePeriod': timePeriod, 'course': course})
            return rendered_page
    else:
        return HttpResponseRedirect('/interface/')

@login_required
def offer_detail(request, idOffer):
    offer = Offer.pickById(idOffer)
    rendered_page = render(request, 'offer_detail.html', {'offer': offer})
    return rendered_page

@login_required        
def offer_edit(request, idOffer):
    offer = Offer.pickById(idOffer)
    if request.method  == 'POST':
        form = OfferForm(request.POST)
        form.updateForm()
        if form.is_valid():
            idProfessor = form.cleaned_data['dropDownProfessor']
            classNumber = form.cleaned_data['classNumber']
            practical = form.cleaned_data['dropDownTeoricaPratica']
            numberOfRegistrations = form.cleaned_data['numberOfRegistrations']
            schedulesIds = form.cleaned_data['listSchedules']
            schedules = [Schedule.pickById(int(schedule)) for schedule in schedulesIds]
            offer.setProfessor(Professor.pickById(idProfessor))
            offer.classNumber = classNumber
            offer.practical = practical
            numberOfRegistrations = None if not numberOfRegistrations else numberOfRegistrations
            offer.setNumberOfRegistrations(numberOfRegistrations)
            offer.setSchedules(schedules)
            offer.store()
            return HttpResponseRedirect('/interface/offer/' + str(idOffer))
    else:
        form = OfferForm(initial={'dropDownProfessor': offer.professor.idProfessor,
                                      'classNumber': offer.classNumber, 
                                      'dropDownTeoricaPratica': offer.practical, 
                                      'numberOfRegistrations': offer.numberOfRegistrations})
        form.updateForm()
        form.fields['listSchedules'].initial = [schedule.idSchedule for schedule in offer.schedules]
    rendered_page = render(request, 'offer_edit.html', {'offer': offer, 'form': form})
    return rendered_page

@login_required
def offer_create(request, idTimePeriod, idCourse):
    timePeriod = TimePeriod.pickById(idTimePeriod)
    course = Course.pickById(idCourse)
    if request.method  == 'POST':
        form = OfferForm(request.POST)
        form.updateForm()
        if form.is_valid():
            idProfessor = form.cleaned_data['dropDownProfessor']
            classNumber = form.cleaned_data['classNumber']
            practical = form.cleaned_data['dropDownTeoricaPratica']
            numberOfRegistrations = form.cleaned_data['numberOfRegistrations']
            schedulesIds = form.cleaned_data['listSchedules']
            schedules = [Schedule.pickById(schedule) for schedule in schedulesIds]
            professor = Professor.pickById(idProfessor)
            practical = (practical == 1)
            offer = Offer(timePeriod, course, classNumber, practical, professor)
            offer.setSchedules(schedules)
            offer.setNumberOfRegistrations(numberOfRegistrations)
            offer.store()
            return HttpResponseRedirect('/interface/offer/' + str(offer.idOffer))
    else:
        form = OfferForm()
        form.updateForm()
    rendered_page = render(request, 'offer_create.html', {'form': form, 'timePeriod': timePeriod, 'course': course})
    return rendered_page

@login_required
def offer_delete(request, idOffer):
    offer = Offer.pickById(idOffer)
    offer.delete()
    return HttpResponseRedirect('/interface/offer/')

@login_required
def offer_list(request):
    form = OfferListForm()
    form.updateForm()
    rendered_page = render(request, 'offer_list.html', {'form': form, })
    return rendered_page

@login_required
def offer_list_generate(request):
    if request.method  == 'POST':
        form = OfferListForm(request.POST)
        form.updateForm()
        if form.is_valid():
            timePeriod = TimePeriod.pickById(int(form.cleaned_data['dropDownTimePeriod']))
            cycleId = int(form.cleaned_data['dropDownCycle'])
            term = int(form.cleaned_data['dropDownTerm'])
            return createPDF(timePeriod, cycleId, term)
    else:
        return HttpResponseRedirect('/interface/offerList')


def createPDF(timePeriod, cycleId, term):
    idealTermCourses = IdealTermCourse.find(idCycle=cycleId, term=term)
    courses = [idealTermCourse.course for idealTermCourse in idealTermCourses]
    allOffers = []
    for course in courses:
        offers = Offer.find(course=course, timePeriod=timePeriod)
        allOffers.append(offers)
    coursesTuple = zip(courses, allOffers)
    faculty = Faculty.find(courseCoordinations = CourseCoordination.find(cycles = [Cycle.pickById(cycleId)]))[0]
    year = int(term/2) + int(term)%2
    title = {}
    title['lines'] = []
    title['lines'].append('Consulta discente sobre o Ensino(CDE)')
    title['lines'].append(str(timePeriod) + ' da ' + faculty.name + u' de Sao Paulo')
    title['lines'].append('Representante de Classe ' + str(year) + u'º ano - ' + Cycle.pickById(cycleId).name)
    name = "".join(letter for letter in str(timePeriod) if ord(letter)<128).replace(' ','')
    name += "_"
    name += "".join(letter for letter in Cycle.pickById(cycleId).name if ord(letter)<128).replace(' ','')
    name += "_"
    name += str(term) + "_Semestre"
    nametex = str(name) + ".tex"
    t = render_to_string('texFiles/offersList.tex', Context({'courses': coursesTuple, 'title': title}))
    l = io.open(nametex, "w", encoding='utf8')
    l.write(t)
    l.close()
    commands.getoutput("pdflatex " + nametex)                              
    commands.getoutput("rm " + name + '.log')
    commands.getoutput("rm " + name + '.aux')
    pdf = file(name + '.pdf').read()
    commands.getoutput("rm " + name + '.tex')
    commands.getoutput("rm " + name + '.pdf')
    response = HttpResponse(pdf)
    response['Content-Type'] = 'application/pdf'
    response['Content-disposition'] = 'attachment; filename=' + name + '.pdf'
    return response
    
    