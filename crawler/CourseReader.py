# coding: utf8
"Object that will read the page of a course"

import datetime
import re

from crawler.Crawler import Crawler, removewhitespaces, appendparameters, \
    getwhatisbetweenthetags
from pulsarInterface.Course import Course
from pulsarInterface.IdealTermCourse import IdealTermCourse


class CourseReader(object):
    """Object that reads the page of a course with a given coursecode and
    inserts all the relevant information in the database"""

    def __init__(self, coursecode, connection, cycle, term, requisitiontype):
        self.coursecode = coursecode
        self.crawler = Crawler()
        self.connection = connection
        self.cycle = cycle
        self.term = term
        self.requisitiontype = requisitiontype

    def scancoursepage(self):
        match = Course.find(courseCode_equal=self.coursecode)
        urlstart = 'https://uspdigital.usp.br/jupiterweb/obterDisciplina'
        parameters = {'sgldis': str(self.coursecode)}
        completeurl = appendparameters(urlstart, parameters)
        self.crawler.loadpage(completeurl)
        name = self.findname()
        startdate = self.findstartdate()
        if match:
            course = match[0]
        else:
            course = Course(self.coursecode, name, startdate)
            aadicionar(course)
            fim = raw_input('Adicionar disciplina?(0 ou 1)')
            if fim == '1':
                course.store()
                print "Stored new course " + str(course.__dict__)
        idealtermmatch = IdealTermCourse.find(idCycle=self.cycle.idCycle,
                                              term=self.term,
                                              idCourse=course.idCourse,
                                              requisitionType=
                                              self.requisitiontype)
        if not idealtermmatch:
            idealterm = IdealTermCourse(self.cycle.idCycle, self.term,
                                        startdate, self.requisitiontype,
                                        course)
            aadicionar(idealterm)
            #fim = raw_input('Adicionar IdealTerm?(0 ou 1)')
            #if fim == '1':
            idealterm.store()
            #    print "Stored new rel_course_cycle " + str(idealterm.__dict__)
        else:
            idealterm = idealtermmatch[0]
        return course

    def findname(self):
        namedata = self.crawler.htmlpage.findAll('b', {})
        # The name will be on the third font tag found
        completename = getwhatisbetweenthetags(unicode(namedata[3]))
        name = completename[22:]  # Disciplina: XXXXXXX - name
        return name

    def findstartdate(self):
        startdatedict = {'class': 'txt_arial_8pt_gray'}
        startdatedata = self.crawler.htmlpage.findAll('span', startdatedict)
        # The startdate will be on the fourth tag found
        completedata = getwhatisbetweenthetags(unicode(startdatedata[4]))
        data = removewhitespaces(completedata)
        data = convertdate(data)
        return data


def convertdate(data):
    data = re.sub('/', '-', data)
    formatdate = '%d-%m-%Y'
    date = datetime.datetime.strptime(data, formatdate)
    formatdate = '%Y-%m-%d'
    data = date.strftime(formatdate)
    return data
