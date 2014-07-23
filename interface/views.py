from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from interface.forms import ProfessorForm, OfferForm
from pulsarInterface.Department import Department
from pulsarInterface.Offer import Offer
from pulsarInterface.Professor import Professor
from pulsarInterface.TimePeriod import TimePeriod
from pulsarInterface.Course import Course

@login_required
def index(request):
    form  = OfferForm()
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
        form = OfferForm(request.POST)
        if form.is_valid():
            timePeriod = TimePeriod.pickById(form.cleaned_data['dropDownTimePeriod'])
            course = Course.pickById(int(form.cleaned_data['dropDownCourse']))
            offers = Offer.find(timePeriod=timePeriod, course=course)
            rendered_page = render(request, 'offer.html', {'offers': offers})
            return rendered_page
    else:
        raise Exception('ERROR')
        