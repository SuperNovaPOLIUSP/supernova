# coding: utf8
"Object that will read a page of a cycle"
import BeautifulSoup
import re
import sys

from crawler.CourseReader import CourseReader
from crawler.Crawler import Crawler
from crawler.Crawler import appendparameters
from crawler.Crawler import getwhatisbetweenthetags
from crawler.OfferReader import OfferReader
from pulsarInterface.Cycle import Cycle
from pulsarInterface.TimePeriod import TimePeriod
from tools.MySQLConnection import MySQLConnection

LASTPERIODDIGIT = -32  # Index of the text where the last digit for the
                       # Period number can be found

COURSES_TO_IGNORE = ['CBM0120','VPS1030']

class CycleReader(object):
    """A reader object which will use a crawler to scan through the page
    of a cycle"""
    def __init__(self):
        self.connection = MySQLConnection()
        self.timeperiod = None
        self.cycle = None
        self.coursereader = None
        self.offerreader = None
        self.crawler = Crawler()
        self.offerreader = OfferReader(self.connection, self.cycle,
                                       self.timeperiod)

    def settimeperiod(self, idtimeperiod):
        "Sets the timeperiod of this cycle by providing its id"
        self.timeperiod = idtimeperiod
        self.offerreader.timeperiod = TimePeriod.pickById(idtimeperiod)

    def setcycle(self, idcycle):
        "Sets the cycle of this reader by searching for the cycle in the bank"
        self.cycle = Cycle.pickById(idcycle)
        self.offerreader.cycle = self.cycle

    def startreadingcycles(self):
        """Starts scanning through the Cycle's page and iterates through each
        of it's courses. This function will not read 'Ciclo Básico' or 'Grande
        Área'"""
        urlstart = 'https://uspdigital.usp.br/jupiterweb/listarGradeCurricular'
        codcg = self.findidfaculty()
        codcurlist = self.findcodcur()
        codhab = str(self.cycle.cycleCode)
        for codcur in codcurlist:
            parameters = {'codcg': str(codcg), 'codcur': str(codcur), 'codhab':
                          codhab, 'tipo': 'N'}
            completeurl = appendparameters(urlstart, parameters)
            self.crawler.loadpage(completeurl)
            coursecodedata = self.crawler.htmlpage.findAll('table', {})
            coursecodedata = coursecodedata[1]  # The table with the courses
            codes = getcoursecodes(coursecodedata)
            if codes:
                break
        return self.startreadingoffers(codes)

    def findidfaculty(self):
        "returns the id of the faculty that has this cycle"
        relations = 'rel_courseCoordination_cycle r1, '\
            'rel_courseCoordination_faculty r2 '
        conditions = 'WHERE r1.idCourseCoordination = r2.idCourseCoordination'\
            ' AND r1.idCycle = ' + str(self.cycle.idCycle)
        query = 'SELECT idFaculty FROM ' + relations + conditions
        results = self.connection.execute(query)
        try:
            idfaculty = results[0][0]
        except IndexError:
            raise IndexError('Não conseguiu achar idFaculty,\
                             checar rel_courseCoordination_cycle e\
                             rel_courseCoordination_faculty com idCycle = ' +
                             str(self.cycle.idCycle))
            sys.exit()
        return idfaculty

    def findcodcur(self):
        """returns the idAcademicProgram representing the code for this
        object's cycle"""
        query = 'SELECT idAcademicProgram FROM rel_academicProgram_cycle '\
                'WHERE idCycle = ' + str(self.cycle.idCycle)
        codcurall = self.connection.execute(query)
        listcodcur = []
        for codcur in codcurall:
            listcodcur.append(codcur[0])
        return listcodcur

    def startreadingoffers(self, coursecodes):
        "Using the coursecodes list, reads all the offers from each code"
        requisitiontypetranslationdict = {0: 1, 1: 2, 2: 3}
        # In the bank: 1 - Obrigatória, 2 - Eletiva, 3 - Livre
        index = 0
        offers = []
        while index < len(coursecodes):
            for period in coursecodes[index]:
                for code in coursecodes[index][period]:
                    if code in COURSES_TO_IGNORE:
                        continue
                    reader = CourseReader(code, self.connection, self.cycle,
                                          period,
                                          requisitiontypetranslationdict
                                          [index])
                    course = reader.scancoursepage()
                    self.offerreader.setcourse(course)
                    offers.extend(self.offerreader.scancourseofferpage())
            index += 1
        return offers


def getcoursecodes(coursecodedata):
    """Returns a list of dictionaries, with the first element pointing to
    mandatory idealterms, and the second element pointing to elective
    idealterms, the third is not evaluated. Each element of the list is a
    dictionary pointing the period to the courses"""
    flag = False
    new_list = []
    requisitiontypedictlist = []
    if not re.match('[\S\s]*Eletivas[\S\s]*', str(coursecodedata)):
        flag = True  # Cycle with no Elective courses
    splitdata = re.split('tr valign="top" bgcolor="#658CCF"',
                         str(coursecodedata))
    for i in splitdata:
        b = BeautifulSoup.BeautifulSoup(i)
        new_list.append(b)
    del new_list[0]  # splitdata[0] has nothing of interest
    for tag in new_list:
        timeperioddict = splittimeperiod(tag)
        coursesdict = {}
        for timeperiodnumber in timeperioddict:
            tag = BeautifulSoup.BeautifulSoup(timeperioddict[timeperiodnumber])
            codes = splitcodes(tag)
            coursesdict[timeperiodnumber] = codes
        requisitiontypedictlist.append(coursesdict)
        if flag:
            requisitiontypedictlist.append([])
            flag = False
    return requisitiontypedictlist


def splitcodes(tag):
    coursecodehtmldict = {'class': 'link_gray'}
    coursecodedata = tag.findAll('a', coursecodehtmldict)
    datalist = []
    for data in coursecodedata:
        data = re.sub('\s', '', str(data))
        # The data will have the format: '<a>course code<\a>'
        data = getwhatisbetweenthetags(data)
        datalist.append(data)
    return datalist


def splittimeperiod(perioddata):
    splitdata = re.split('Período Ideal', str(perioddata))
    index = 0
    timeperioddict = {}
    while(index < len(splitdata) - 1):
    # -1 because the last relevant number is in the penultimate
    # element of the list
        lastdigit = splitdata[index][LASTPERIODDIGIT]
        possibledigit = splitdata[index][LASTPERIODDIGIT-1]
        if re.match('\d', possibledigit):
            timeperiodnumber = int(possibledigit + lastdigit)
        else:
            timeperiodnumber = int(lastdigit)  # Position of the Period number
        timeperioddict[timeperiodnumber] = splitdata[index + 1]
        index += 1
    return timeperioddict
