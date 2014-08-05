# coding: utf8
"Object that will read the offering page of a course"

import re
import sys

from crawler.Crawler import Crawler
from crawler.Crawler import appendparameters
from crawler.Crawler import getwhatisbetweenthetags
from crawler.Crawler import removewhitespaces
from pulsarInterface.Course import Course
from pulsarInterface.Offer import Offer
from pulsarInterface.Professor import Professor
from pulsarInterface.Schedule import Schedule


class OfferReader(object):
    """A reader object which will use a crawler to scan through the page
    describing the offers of a course"""

    def __init__(self, connection, cycle, timeperiod):
        self.connection = connection
        self.timeperiod = timeperiod
        self.cycle = cycle
        self.crawler = Crawler()
        self.course = None

    def setcourse(self, course):
        "Sets the course which will be scanned"
        if not isinstance(course, Course):
            raise Exception('Invalid course parameter')
        self.course = course

    def scancourseofferpage(self):
        "Scans the page of the course, adding new offers to the bank"
        urlstart = 'https://uspdigital.usp.br/jupiterweb/obterTurma'
        fullurl = appendparameters(urlstart, {'sgldis':
                                              self.course.courseCode})
        self.crawler.loadpage(fullurl)
        offers = []
        if re.match('[\S\s]*Hor&aacute;rio[\S\s]*',
                    str(self.crawler.htmlpage)):
            offersdata = self.getrelevantdata()
            offers.extend(self.createoffers(offersdata))
        return offers

    def checkprofessor(self, professorname):
        """Checks if the professor with the name passed as argument is already
        in the bank and, if it isn't, stores a new professor. After that,
        returns the Professor object. If the professor name is empty, there is
        a special entry in the bank for this case """
        professor = Professor.find(name_equal=professorname)
        if not professor:
            if not professorname:
                professor = Professor.pickById(5870)
                # ID: 5870 = SEM PROFESSOR
            else:
                professor = Professor(professorname)
                professor.store()
        else:
            professor = professor[0]
        return professor

    def checkschedule(self, sched):
        """Checks if the schedule object passed as sched is already in the
        bank and, if it isn't, stores a new schedule"""
        if not sched.idSchedule:
            sched.store()

    def generateoffer(self, classn_pract, prof_sched_info, professorname):
        """Creates a new Offer object with the informations about the class
        number and practical (classn_pract), the professor and the schedules
        (prof_sched_info), note that the professor that will be associated with
        this offer has its name in professorname"""
        professor = self.checkprofessor(professorname)
        offer = Offer(self.timeperiod, self.course, classn_pract[0],
                      classn_pract[1],
                      professor)
        if not isinstance(prof_sched_info[1], list):
            prof_sched_info[1] = [prof_sched_info[1]]
        for sched in prof_sched_info[1]:
            self.checkschedule(sched)
        offer.setSchedules(prof_sched_info[1])
        return offer

    def createoffers(self, offersdata):
        "Returns a list of offers to treat"
        offerslist = []
        for offerdata in offersdata:
            classn_pract = getclassnunmberandpractical(offerdata[0])
            prof_sched = getprofessorandschedule(offerdata[1])
            prof_sched = organize(prof_sched)
            for prof_sched_info in prof_sched:
                for professorname in prof_sched_info[0]:
                    offer = self.generateoffer(classn_pract, prof_sched_info,
                                               professorname)
                    offerslist.append(offer)
        return offerslist

    def getrelevantdata(self):
        """Returns a list of tuple with tag objects, each one containing
        information of one offer related to a course. The first element
        of the tuple has the classnumber and practical information, the
        second element has the professor and schedule data"""
        tables = self.crawler.htmlpage.findAll('table')[1]
        tables = tables.findAll('table')[0]
        tables = tables.findAll('table')[5]
        tables = tables.findAll('table')
        for table in tables:
            if re.match('[\S\s]*Didáticas[\S\s]*', str(table)):
                tables.remove(table)
        # Some irrelevant data will appear with strides of size 3 in this list
        tables = removefromlistwithstridesize(tables, 2, 2)
        return group(tables, 2)


def getclassnunmberandpractical(datatag):
    """Returns a tuple in which the first value represents the classnumber
    of this offer and the second value represents if the offer is
    practical"""
    infodict = {'class': 'txt_arial_8pt_gray'}
    informationdata = datatag.findAll('span', infodict)
    classnumber = refineclassnumber(informationdata[0])
    practical = refinepractical(informationdata[3])
    return (classnumber, practical)


def checktotime(text):
    """ Returns a match object with information related to the match of the
    text to a timestamp string like 'HH:MM' or 'MM:HH' """
    return re.match('\d\d:\d\d', text)


def checkadditionalprofessors(days, informationdata, index, professorname,
                              increment, decrement):
    """Checks for extra professors in the same schedule of an offer, requires
    the index of the set of information being scanned"""
    firstname = getutxt(informationdata[index + increment + 2])
    professorname.append(firstname)
    additionalprofessors = 0
    while (index + increment + 2 + additionalprofessors + 1 <
           len(informationdata)):
        # index --> The index of the previous loop, which means the individual
        #     schedule with the professors
        # +2 to ignore the first 2 timestamps
        # +1 to bypass the first professor name
        nextword = getutxt(informationdata[index + 3 +
                           additionalprofessors + 1 - decrement])
        if (nextword not in days and not checktotime(nextword)):
        # While the next entries are not weekdays or time HH:MM
            additionalprofessors += 1
            professorname.append(getutxt(informationdata[index + increment + 2
                                         + additionalprofessors]))
        else:
            break
    return additionalprofessors


def getprofessorandschedule(datatag):
    """Returns a tuple in which the first value represents a list of professors
    and the second value represents a list of schedules"""
    days = {u'dom': u'Domingo', u'seg': u'Segunda', u'ter': u'Terça',
            u'qua': u'Quarta', u'qui': u'Quinta', u'sex': u'Sexta',
            u'sab': u'Sabado'}
    infodict = {'class': 'txt_arial_8pt_gray'}
    informationdata = datatag.findAll('span', infodict)
    index = 0
    prof_sched = []
    while index < len(informationdata):
        professorname = []
        text = getutxt(informationdata[index])
        if text in days:  # Traditional format
            day = text
            increment = 1  # The day of the week is the first word read
            decrement = 0  # No need to go back a word
        elif checktotime(text):
            increment = 0
            # Without the day of the week, there's no need to bypass a word
            decrement = 1
            # But you need to go back a word to find the next professors
        else:  # Starting with schedule or with another professor
            schedule = None
            professorname.append(informationdata[index])
            index += 3
        start = getutxt(informationdata[index + increment]) + ':00'  # seconds
        end = getutxt(informationdata[index + increment + 1]) + ':00'
        schedule = checkforschedule(days[day], start, end)
        additionalprofessors = checkadditionalprofessors(days, informationdata,
                                                         index,
                                                         professorname,
                                                         increment,
                                                         decrement)
        index += increment + 3 + additionalprofessors
        prof_sched.append((professorname, [schedule]))
    return prof_sched


def getutxt(tag):
    """Return an unicode string representing the text inside the tags of
    the tag object passed as parameter"""
    return getwhatisbetweenthetags(unicode(tag))


def treatoffers(offers):
    "Inserts or updates the list of offers"
    for offer in offers:
        possiblematches = Offer.find(course=offer.course,
                                     professor=offer.professor,
                                     timePeriod=offer.timePeriod,
                                     classNumber=offer.classNumber,
                                     practical=offer.practical)
        # What can happen here?
        # 1 - Offer as a whole already exists in bank
        if(len(possiblematches) > 1):
            sys.exit()
        elif (offer.idOffer is not None or offer in possiblematches):
            pass
        else:
        # 2 - Offer as a whole is not in bank, maybe the schedules
        # have changed.
            if possiblematches:
                for duplicate in possiblematches:
                    if not comparelistsofschedules(duplicate.schedules,
                                                   offer.schedules):
                        updateschedulesoffer(duplicate, offer)
            else:
        # 3 - Offer as a whole is not in the bank, and there is no offer with
        # the same data but different schedules in the bank, maybe the
        # professor changed?
                possiblematches = Offer.find(course=offer.course,
                                             timePeriod=offer.timePeriod,
                                             classNumber=offer.classNumber,
                                             practical=offer.practical,
                                             schedule=offer.schedules[0])
                if possiblematches:
                    # In this case, even if the schedules have also changed,
                    # the store() method will take care of it
                    for match in possiblematches:
                        updateprofessoroffer(match, offer)
                else:
        # 4 - No similar offer is in the bank, it must be stored now
                    storenewoffer(offer)
            # offer.store()
            # print offer.__dict__


def updateschedulesoffer(oldoffer, newoffer):
    oldoffer.setSchedules(newoffer.schedules)
    oldoffer.store()

def updateprofessoroffer(oldoffer, newoffer):
    oldoffer.professor = newoffer.professor
    oldoffer.store()


def storenewoffer(offer):
    offer.store()


def checkforschedule(day, start, end):
    """Returns a schedule object created after a bank query using the
    parameters or a new schedule, if a schedule is not found"""
    schedule = Schedule.find(dayOfTheWeek_equal=day,
                             start_equal=start,
                             end_equal=end)
    if schedule:
        schedule = schedule[0]
    else:
        schedule = Schedule(day, end, 'semanal', start)
    return schedule


def linkprofessornametoschedule(professorname, schedule, profscheduledict):
    """Adds a relation of the professorname and schedule passed as parameter to
    the dictionary"""
    if professorname not in profscheduledict.keys():
        profscheduledict[professorname] = [schedule]
    else:
        profscheduledict[professorname].append(schedule)


def refineclassnumber(htmltag):
    "Returns the class number from the tagobject passed as parameter"
    htmltag = unicode(htmltag)
    # The format of the number is: <span>number</span>
    classnumber = getwhatisbetweenthetags(htmltag)
    classnumber = removewhitespaces(classnumber)
    # The number format is YYYYPN+ where the important part is the N
    # Y corresponds to the year, P corresponds to the period
    classnumber = classnumber[5:]
    # Some of the classnumbers have letters on them
    # This is the default way of dealing with it
    if re.match('[ABCDEF]', classnumber[0]) or re.match('[ABCDEF]',
                                                        classnumber[1]):
        classnumber = int(classnumber, 16)
    else:
        # Some of the pages include additional text/information on the same
        # line
        classnumber = re.sub('\D', '', classnumber)
        classnumber = int(classnumber)
    return classnumber


def refinepractical(htmltag):
    """Returns True if the course being read is practical on this offer, false
    otherwise"""
    htmltag = unicode(htmltag)
    # The format of the number is: <span>number</span>
    practical = getwhatisbetweenthetags(htmltag)
    practical = removewhitespaces(practical)
    # If it is 'Teórica', then it's not practical
    if practical == u'Teórica' or practical == u'TeóricaVinculada':
        return False
    return True


def group(lst, nbr):
    """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]
       Group a list into consecutive n-tuples. Incomplete tuples are
       discarded e.g.  >>> group(range(10), 3)

       [(0, 1, 2), (3, 4, 5), (6, 7, 8)]"""
    for i in range(0, len(lst), nbr):
        val = lst[i:i + nbr]
        if len(val) == nbr:
            yield tuple(val)


def removefromlistwithstridesize(lst, stride, firstocurrence):
    """Removes elements from a list taht appear with a pattern of one
    ocurrence after stride steps, starting with the first ocurrence.
    Returns the list at the end"""
    index = firstocurrence
    while index < len(lst):
        lst.remove(lst[index])
        index += stride  # -1 because the number of elements is lower
    return lst


def organize(mat):
    """ Organizes schedules and professor names from the matrix parameter """
    index = len(mat) - 1
    mat = [list(i) for i in mat]
    while(index > 0):
        lst = []
        index2 = 0
        while(index2 < index):
            if mat[index][0] == mat[index2][0]:
                lst.extend(mat[index][1])
                lst.extend(mat[index2][1])
                mat[index][1] = lst
                del mat[index2]
                break
            else:
                index2 += 1
        index -= 1
    return mat


def comparelistsofschedules(schedlist1, schedlist2):
    """Returns true if all elements of schedlist1 are in schedlist2 and
    vice-versa"""
    for schedule in schedlist1:
        if schedule not in schedlist2:
            return False
    for schedule in schedlist2:
        if schedule not in schedlist1:
            return False
    return True
