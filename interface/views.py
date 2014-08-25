#coding: utf8
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from interface.forms import ProfessorForm, IndexForm, OfferForm
from login.models import Log
from login.views import get_time
from pulsarInterface.Course import Course
from pulsarInterface.Department import Department
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
            professor_name_old = professor.name
            professor_memberId_old = professor.memberId
            professor_office_old = professor.office
            professor_email_old = professor.email
            professor_phoneNumber_old = professor.phoneNumber
            professor_cellphoneNumber_old = professor.cellphoneNumber
            professor_idDepartment_old = professor.idDepartment
            professor.name = name
            professor.memberId = memberId
            office = None if not office else office
            email = None if not email else email
            professor.office = office
            professor.email = email
            professor.phoneNumber = phoneNumber
            professor.cellphoneNumber = cellphoneNumber
            professor.idDepartment = idDepartment
            user= request.user
            user_name = request.user.username
            time = get_time()
            action = "Usuário " + str(user_name) + " alterou as informações do professor " + str(professor_name_old) \
            + " { name: " + str(professor_name_old) + " => " + str(professor.name) \
            + "; memberId: " + str(professor_memberId_old) + " => " + str(professor.memberId) \
            + "; office: " + str(professor_office_old) + " => " + str(professor.office) \
            + "; email: " + str(professor_email_old) + " => " + str(professor.email) \
            + "; phoneNumber: " + str(professor_phoneNumber_old) + " => " + str(professor.phoneNumber) \
            + "; cellphoneNumber: " + str(professor_cellphoneNumber_old) + " => " + str(professor.cellphoneNumber) \
            + "; idDepartment: " + str(professor_idDepartment_old) + " => " + str(professor.idDepartment) + " }"
            professor_edit_log = Log(user=user, action=action, time=time)
            professor_edit_log.save()
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
    user= request.user
    user_name = request.user.username
    time = get_time()
    action = "Usuário " + str(user_name) + " deletou o professor " + str(professor.name)
    professor_delete_log = Log(user=user, action=action, time=time)
    professor_delete_log.save()
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
            user= request.user
            user_name = request.user.username
            time = get_time()
            action = "Usuário " + str(user_name) + " criou o professor " + str(name)
            professor_create_log = Log(user=user, action=action, time=time)
            professor_create_log.save()
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
            schedules_string_old = [str(schedule) for schedule in offer.schedules]
            schedules_string = [str(schedule) for schedule in schedules]
            user= request.user
            user_name = request.user.username
            time = get_time()
            action = "Usuário " + str(user_name) + " editou o oferecimento id: " + str(offer.idOffer) + " {" \
            + " Código do Curso: " + str(offer.course.courseCode) \
            + "; Periodo: " + str(offer.timePeriod) \
            + "; Turma: T" + str(offer.classNumber) + " => T" + str(classNumber) \
            + "; Professor: " + str(offer.professor.name) + " => " + str(Professor.pickById(idProfessor).name) \
            + "; Horários: " + str(schedules_string_old) +  " => " + str(schedules_string) + " }"
            offer_edit_log = Log(user=user, action=action, time=time)
            offer_edit_log.save()
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
            user= request.user
            user_name = request.user.username
            time = get_time()
            schedules_string = [str(schedule) for schedule in schedules]
            action = "Usuário " + str(user_name) + " criou o oferecimento id: " + str(offer.idOffer) + " {" \
            + " Código do Curso: " + str(course.courseCode) \
            + "; Turma: T" + str(classNumber) \
            + "; Professor: " + str(professor.name) \
            + "; Periodo: " + str(timePeriod) \
            + "; Horários: " + str(schedules_string) + " }"
            offer_create_log = Log(user=user, action=action, time=time)
            offer_create_log.save()
            return HttpResponseRedirect('/interface/offer/' + str(offer.idOffer))
    else:
        form = OfferForm()
        form.updateForm()
    rendered_page = render(request, 'offer_create.html', {'form': form, 'timePeriod': timePeriod, 'course': course})
    return rendered_page

@login_required
def offer_delete(request, idOffer):
    offer = Offer.pickById(idOffer)
    user= request.user
    user_name = request.user.username
    time = get_time()
    schedules_string = [str(schedule) for schedule in offer.schedules]
    action = "Usuário " + str(user_name) + " deletou o oferecimento id: " + str(offer.idOffer) + " {" \
    + " Código do Curso: " + str(offer.course.courseCode) \
    + "; Turma: T" + str(offer.classNumber) \
    + "; Professor: " + str(offer.professor.name) \
    + "; Periodo: " + str(offer.timePeriod) \
    + "; Horários: " + str(schedules_string) + " }"
    offer_delete_log = Log(user=user, action=action, time=time)
    offer_delete_log.save()
    offer.delete()
    return HttpResponseRedirect('/interface/offer/') 