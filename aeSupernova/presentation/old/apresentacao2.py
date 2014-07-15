#Embedded file name: /home/www/aeSupernova/aeSupernova/presentation/apresentacao2.py
from pulsarInterface.OpticalSheet import *
import commands

def findReports(timePeriodData, facultyData, cycleData, termData):
    if timePeriodData != 0 and facultyData == cycleData == termData == 0:
        timePeriodData2 = TimePeriod.pickById(timePeriodData)
        offers = Offer.find(timePeriodData2)
        session = timePeriodData2.session
        year = timePeriodData2.year
        courses = []
        terms = []
        idCycles = []
        cycles = []
        reports = []
        courseCoordinations = Coursecoordination.find()
        faculties = Faculty.find()
        for offer in offers:
            courses.append(Course.pickById(offer.idCourse))

        for course in courses:
            idealTermCourses = IdealTermCourse.find(course.idCourse)
            for idealtermCourse in idealTermCourses:
                terms.append(idealTermCourse.term)

            for term in terms:
                for idealTermCourse in idealTermCourses:
                    idCycles.append(idealTermCourse.idCycle)

                for idCycle in idCycles:
                    cycles.append(Cycle.pickById(idCycle))

                for cycle in cycles:
                    for courseCoordination in courseCoordinations:
                        if cycle in courseCoordination.cycles:
                            for faculty in faculties:
                                if courseCoordination in faculty.courseCoordinations:
                                    if {'year': {'name': year,
                                              'id': year},
                                     'session': {'name': session,
                                                 'id': session},
                                     'faculty': {'name': faculty.name,
                                                 'id': faculty.idFaculty},
                                     'cycle': {'name': cycle.name,
                                               'id': cycle.idCycle},
                                     'term': {'name': term,
                                              'id': term},
                                     'course': {'name': course.name,
                                                'id': course.idCourse}} not in reports:
                                        reports.append({'year': {'name': year,
                                                  'id': year},
                                         'session': {'name': session,
                                                     'id': session},
                                         'faculty': {'name': faculty.name,
                                                     'id': faculty.idFaculty},
                                         'cycle': {'name': cycle.name,
                                                   'id': cycle.idCycle},
                                         'term': {'name': term,
                                                  'id': term},
                                         'course': {'name': course.name,
                                                    'id': course.idCourse}})

    elif timePeriodData != 0 and facultyData != 0 and cycleData == termData == 0:
        timePeriodData2 = TimePeriod.pickById(timePeriodData)
        offers = Offer.find(timePeriodData2)
        session = timePeriodData2.session
        year = timePeriodData2.year
        courses = []
        terms = []
        idCycles = []
        cycles = []
        reports = []
        faculty = Faculty.pickById(facultyData)
        for offer in offers:
            courses.append(Course.pickById(offer.idCourse))

        for course in courses:
            idealTermCourses = IdealTermCourse.find(course.idCourse)
            for idealtermCourse in idealTermCourses:
                terms.append(idealTermCourse.term)

            for term in terms:
                for idealTermCourse in idealTermCourses:
                    idCycles.append(idealTermCourse.idCycle)

                for idCycle in idCycles:
                    cycles.append(Cycle.pickById(idCycle))

                for cycle in cycles:
                    if {'year': {'name': year,
                              'id': year},
                     'session': {'name': session,
                                 'id': session},
                     'faculty': {'name': faculty.name,
                                 'id': faculty.idFaculty},
                     'cycle': {'name': cycle.name,
                               'id': cycle.idCycle},
                     'term': {'name': term,
                              'id': term},
                     'course': {'name': course.name,
                                'id': course.idCourse}} not in reports:
                        reports.append({'year': {'name': year,
                                  'id': year},
                         'session': {'name': session,
                                     'id': session},
                         'faculty': {'name': faculty.name,
                                     'id': faculty.idFaculty},
                         'cycle': {'name': cycle.name,
                                   'id': cycle.idCycle},
                         'term': {'name': term,
                                  'id': term},
                         'course': {'name': course.name,
                                    'id': course.idCourse}})

    elif timePeriodData != 0 and facultyData != 0 and cycleData != 0 and termData == 0:
        timePeriodData2 = TimePeriod.pickById(timePeriodData)
        offers = Offer.find(timePeriod=timePeriodData2)
        session = timePeriodData2.session
        year = timePeriodData2.year
        courses = []
        terms = []
        reports = []
        faculty = Faculty.pickById(facultyData)
        cycle = Cycle.pickById(cycleData)
        for offer in offers:
            courses.append(Course.pickById(offer.idCourse))

        for course in courses:
            idealTermCourses = IdealTermCourse.find(course.idCourse)
            for idealtermCourse in idealTermCourses:
                terms.append(idealTermCourse.term)

            for term in terms:
                if {'year': {'name': year,
                          'id': year},
                 'session': {'name': session,
                             'id': session},
                 'faculty': {'name': faculty.name,
                             'id': faculty.idFaculty},
                 'cycle': {'name': cycle.name,
                           'id': cycle.idCycle},
                 'term': {'name': term,
                          'id': term},
                 'course': {'name': course.name,
                            'id': course.idCourse}} not in reports:
                    reports.append({'year': {'name': year,
                              'id': year},
                     'session': {'name': session,
                                 'id': session},
                     'faculty': {'name': faculty.name,
                                 'id': faculty.idFaculty},
                     'cycle': {'name': cycle.name,
                               'id': cycle.idCycle},
                     'term': {'name': term,
                              'id': term},
                     'course': {'name': course.name,
                                'id': course.idCourse}})

    else:
        timePeriodData2 = TimePeriod.pickById(timePeriodData)
        offers = Offer.find(timePeriod = timePeriodData2)
        session = timePeriodData2.session
        year = timePeriodData2.year
        courses = []
        term = termData
        reports = []
        faculty = Faculty.pickById(facultyData)
        cycle = Cycle.pickById(cycleData)
        for offer in offers:
            courses.append(Course.pickById(offer.idCourse))

        for course in courses:
            if {'year': {'name': year,
                      'id': year},
             'session': {'name': session,
                         'id': session},
             'faculty': {'name': faculty.name,
                         'id': faculty.idFaculty},
             'cycle': {'name': cycle.name,
                       'id': cycle.idCycle},
             'term': {'name': term,
                      'id': term},
             'course': {'name': course.name,
                        'id': course.idCourse}} not in reports:
                reports.append({'year': {'name': year,
                          'id': year},
                 'session': {'name': session,
                             'id': session},
                 'faculty': {'name': faculty.name,
                             'id': faculty.idFaculty},
                 'cycle': {'name': cycle.name,
                           'id': cycle.idCycle},
                 'term': {'name': term,
                          'id': term},
                 'course': {'name': course.name,
                            'id': course.idCourse}})

    return reports


def getReport(length, year, session, reports):
    if lenght == 1:
        length = 's'
    else:
        length = 'q'
    fileName = []
    for report in reports:
        course = report['course']
        courseId = course['id']
        course = Course.pickById(courseId)
        courseCode = course.courseCode
        fileName.append('cde' + year + lenght + session + 'a1_' + courseCode + '.pdf')

    return fileName[0]
