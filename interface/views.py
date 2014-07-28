#coding: utf8
from django import forms
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from interface.forms import ProfessorForm, IndexForm, OfferForm, getKey
import json
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
def search_courses(request):
    if request.REQUEST['term']:
        q = request.GET.get('term', '')
        courses = Course.find(courseCode_like=q)
        result_courses = []
        for course in courses:
            course_json = {}
            course_json['id'] = course.idCourse
            course_json['label'] = course.courseCode
            course_json['value'] = course.courseCode
            result_courses.append(course_json)
        data = json.dumps(result_courses)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required
def crawler(request):
    rendered_page = render(request, 'crawler.html', {})
    return rendered_page


@login_required
def crawler_run(request):
    if request.method == 'POST':
        print 'working'
