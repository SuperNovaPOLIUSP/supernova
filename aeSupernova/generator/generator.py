from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from pulsarInterface.IdealTermCourse import *
from aeSupernova.generator.CourseGenerator import *
from aeSupernova.header.Header import *


#from aeSupernova.generator.CourseReportGenerator import *
@login_required
def openSite(request):      
    header = Header()
    header.setTermFunction('loadCourses($("#headerTimePeriod").val(),$("#headerCycle").val(),$("#headerTerm").val())')
    return render_to_response('generator.html',{'header':header.getHtml()})


def loadCourses(request):
    data = request.GET
    #idealTermCourses = IdealTermCourse.find(idCycle = int(data['idCycle']), term = int(data['term']), endDate_equal = '0000-00-00')
    #courses = []
    #for idealTermCourse in idealTermCourses:
    #    course = {}
    #    course['name'] = idealTermCourse.course.name
    #    course['idCourse'] = idealTermCourse.course.idCourse
    #    courses.append(course)
    cursor = MySQLConnection()
    coursesData = cursor.execute('SELECT course.idCourse, course.name FROM rel_cycle_opticalSheet JOIN aggr_opticalSheetField on aggr_opticalSheetField.idOpticalSheet = rel_cycle_opticalSheet.idOpticalSheet JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer JOIN course ON course.idCourse = aggr_offer.idCourse WHERE idTimePeriod = ' + str(data['idTimePeriod']) + ' AND idCycle = ' + str(data['idCycle']) + ' AND term = ' + str(data['term']) + ' GROUP BY idCourse')
    courses = [] 
    for courseData in coursesData:
        course = {}
        course['name'] = courseData[1]
        course['idCourse'] = courseData[0]
        courses.append(course)
    assessmentsData = cursor.execute('SELECT aggr_survey.assessmentNumber FROM rel_cycle_opticalSheet JOIN aggr_opticalSheetField on aggr_opticalSheetField.idOpticalSheet = rel_cycle_opticalSheet.idOpticalSheet JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer JOIN aggr_survey ON aggr_survey.idOpticalSheet = rel_cycle_opticalSheet.idOpticalSheet WHERE idTimePeriod = ' + str(data['idTimePeriod']) + ' AND idCycle = ' + str(data['idCycle']) + ' AND term = ' + str(data['term']) + ' GROUP BY aggr_survey.assessmentNumber')
    assessments = [int(assessment[0]) for assessment in assessmentsData]
    response = {}
    response['courses'] = courses
    response['assessments'] = assessments
    return HttpResponse(json.dumps(response)) 

def generateCourses(request):
    data = request.GET
    idCourses = json.loads(data['idCourses']) #Do something with this list
    idCourses = [int(idCourse) for idCourse in idCourses]
    if int(data['useProfessorsName']) == 1:
         useProfessorsName = True
    else:
        useProfessorsName = False

    if int(data['byOffer']) == 1:
        byOffer = True
    else:
        byOffer = False
    idTimePeriod = int(data['idTimePeriod'])
    idFaculty = int(data['idFaculty'])
    assessmentNumber = int(data['assessmentNumber'])
    
    #return HttpResponse(str(idTimePeriod)+'brisa'+str(idCourses)+ str(useProfessorsName)+ str(byOffer)+ str(idFaculty)+'brisa'+str(assessmentNumber))
    CourseReportGenerator(idTimePeriod, idCourses, useProfessorsName, byOffer, idFaculty, assessmentNumber)

    print idTimePeriod
    print idCourses
    print useProfessorsName
    print byOffer
    print idFaculty
    print assessmentNumber

    return HttpResponse('ok')
