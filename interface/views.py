#coding: utf8
import commands
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.context import Context
from django.template.loader import render_to_string
import io
from interface.forms import ProfessorForm, IndexForm, OfferForm, OfferListForm
from login.models import Log
from login.views import get_time
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

from pulsarInterface.Cycle import Cycle
from pulsarInterface.Offer import Offer

from interface.forms import ProfessorForm, CrawlerForm, CrawlerResultsForm, offer_to_string
from crawler.CycleReader import CycleReader

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
            action = u"Usuário " + user_name + u" alterou as informações do professor " + professor_name_old \
            + u" { name: " + professor_name_old + " => " + professor.name \
            + u"; memberId: " + str(professor_memberId_old) + " => " + str(professor.memberId) \
            + u"; office: " + str(professor_office_old) + " => " + str(professor.office) \
            + u"; email: " + str(professor_email_old) + " => " + str(professor.email) \
            + u"; phoneNumber: " + str(professor_phoneNumber_old) + " => " + str(professor.phoneNumber) \
            + u"; cellphoneNumber: " + str(professor_cellphoneNumber_old) + " => " + str(professor.cellphoneNumber) \
            + u"; idDepartment: " + str(professor_idDepartment_old) + " => " + str(professor.idDepartment) + " }"
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
    action = u"Usuário " + user_name + u" deletou o professor " + professor.name
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
            action = u"Usuário " + user_name + u" criou o professor " + name
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
            schedules_string_old = '[ '
            schedules_string = '[ '
            for schedule in offer.schedules:
                schedules_string_old += str(schedule).replace('ç','c') + " "
            for schedule in schedules:
                schedules_string += str(schedule).replace('ç','c') + " "
            schedules_string_old += ']'
            schedules_string += ']'
            user= request.user
            user_name = request.user.username
            time = get_time()
            action = u"Usuário " + user_name + u" editou o oferecimento id: " + str(offer.idOffer) + " {" \
            + u" Código do Curso: " + str(offer.course.courseCode) \
            + u"; Periodo: " + str(offer.timePeriod) \
            + u"; Turma: T" + str(offer.classNumber) + " => T" + str(classNumber) \
            + u"; Professor: " + offer.professor.name + " => " + Professor.pickById(idProfessor).name \
            + u"; Horários: " + schedules_string_old +  " => " + schedules_string + " }"
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
            schedules_string = '[ '
            for schedule in schedules:
                schedules_string += str(schedule).replace('ç','c') + " "
            schedules_string += ']'
            action = u"Usuário " + user_name + u" criou o oferecimento id: " + str(offer.idOffer) + " {" \
            + u" Código do Curso: " + str(course.courseCode) \
            + u"; Turma: T" + str(classNumber) \
            + u"; Professor: " + professor.name \
            + u"; Periodo: " + str(timePeriod) \
            + u"; Horários: " + schedules_string + " }"
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
    schedules_string = '[ '
    for schedule in offer.schedules:
        schedules_string += str(schedule).replace('ç','c') + " "
    schedules_string += ']'
    action = u"Usuário " + user_name + u" deletou o oferecimento id: " + str(offer.idOffer) + " {" \
    + u" Código do Curso: " + str(offer.course.courseCode) \
    + u"; Turma: T" + str(offer.classNumber) \
    + u"; Professor: " + offer.professor.name \
    + u"; Periodo: " + str(offer.timePeriod) \
    + u"; Horários: " + schedules_string + " }"
    offer_delete_log = Log(user=user, action=action, time=time)
    offer_delete_log.save()
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
    if term != 0:
        idealTermCourses = IdealTermCourse.find(idCycle=cycleId, term=term)
        year = int(term/2) + int(term)%2
    else:
        idealTermCourses = IdealTermCourse.find(idCycle=cycleId)
        year = "Todos"
    courses = [idealTermCourse.course for idealTermCourse in idealTermCourses]
    allOffers = []
    for course in courses:
        offers = Offer.find(course=course, timePeriod=timePeriod)
        allOffers.append(offers)
    coursesTuple = zip(courses, allOffers)
    faculty = Faculty.find(courseCoordinations = CourseCoordination.find(cycles = [Cycle.pickById(cycleId)]))[0]
    path = settings.MEDIA_ROOT + 'pdf/'
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
    name = name.replace('/','_') #Bugfix - Names with '/' do not go well in an Unix environment
    t = render_to_string('texFiles/offersList.tex', Context({'courses': coursesTuple, 'title': title}))
    l = io.open(str(path) + str(name) + ".tex", "w", encoding='utf8')
    l.write(t)
    l.close()
    commands.getoutput("pdflatex -interaction=nonstopmode -output-directory=" + str(path) + " " + str(path) + str(name) + '.tex')                                         
    commands.getoutput("rm " + str(path) + str(name) + '.log')
    commands.getoutput("rm " + str(path) + str(name) + '.aux')
    pdf = file(str(path) + str(name) + '.pdf').read()
    commands.getoutput("rm " + str(path) + str(name) + '.tex')
    commands.getoutput("rm " + str(path) + str(name) + '.pdf')
    response = HttpResponse(pdf)
    response['Content-Type'] = 'application/pdf'
    response['Content-disposition'] = 'attachment; filename=' + name + '.pdf'
    return response

@login_required
def crawler(request):
    form = CrawlerForm()
    rendered_page = render(request, 'crawler.html', {'form': form})
    return rendered_page


def crawler_results(request, offers):
    offers_inserted = []
    for offer in offers:
        if not Offer.find(course=offer.course, professor=offer.professor,
                          timePeriod=offer.timePeriod,
                          classNumber=offer.classNumber,
                          practical=offer.practical):
            offer.store()
            offers_inserted.append(offer_to_string(offer))
            rendered_page = render(request, 'crawler_results.html',
                                   {'offers': offers_inserted})
    return rendered_page


@login_required
def crawler_run(request):
    if request.method == 'POST':
        form = CrawlerForm(request.POST)
        if form.is_valid():
            id_time_period = form.cleaned_data['timePeriod']
            ids_cycle = [int(id_cycle) for id_cycle in form.cleaned_data['cycle']]
            offers = []
            for id_cycle in ids_cycle:
                crawler = CycleReader()
                crawler.settimeperiod(id_time_period)
                crawler.setcycle(id_cycle)
                offers_obtained = crawler.startreadingcycles()
                offers.extend(offers_obtained)
            return crawler_results(request, offers)
    return HttpResponseRedirect('/interface/crawler/')
