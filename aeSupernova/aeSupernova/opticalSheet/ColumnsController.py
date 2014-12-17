from pulsarInterface.Course import Course
from pulsarInterface.Offer import Offer
from pulsarInterface.Professor import Professor
from pulsarInterface.TimePeriod import TimePeriod
from tools.MySQLConnection import MySQLConnection


class ColumnsControllerError(Exception):
    """
     Exception reporting an error in the execution of a ColumnsController method.

    :version:
    :author:
    """
    pass

class ColumnsController(object):

    """
     

    :version:
    :author:
    """

    @staticmethod
    def findCourses(searchedAbbreviation, searchedCourseCode, searchedName, idTimePeriod, idCycle = None, term = None):
        """
         returns a list of dicts containig the keys: courseName, courseAbbreviation,
         courseCode and idCourse.

        @param string searchedAbbreviation : Part of the wanted course's abbreviation.
        @param string searchedCourseCode : Part of the wanted course's courseCode
        @param string searchedName : Part of the wanted course's name.
        @param int idTimePeriod : The idTimePeriod of the wanted course's timePeriod.
        @param int idCycle : Is None by default, if it is set the courses related to the chosen cycle will be the firsts of the returned list.
        @param int term : The term related to the idCycle, is None by default.
        @return [] :
        @author
        """
        cursor = MySQLConnection()
        activeIdCourses = cursor.execute('SELECT idCourse FROM aggr_offer WHERE idTimePeriod = ' + str(idTimePeriod) + ' GROUP BY idCourse')
        activeIdCourses = [course[0] for course in activeIdCourses]
        firstIdCourses = []
        if idCycle != None or term != None:
            query = 'SELECT idCourse FROM rel_course_cycle WHERE endDate = "0000-00-00"'
            if idCycle != None:
                query = query + ' AND idCycle = ' + str(idCycle)
            if term != None:
                query = query + ' AND term = ' + str(term)
            firstIdCourses = cursor.execute(query)
            firstIdCourses = [course[0] for course in firstIdCourses]
            
        courses = Course.find(abbreviation_like = searchedAbbreviation, courseCode_like = searchedCourseCode, name_like = searchedName, endDate_equal = '0000-00-00', idCourse = activeIdCourses)
        finalList = []
        for course in courses:
            dictCourse = {}
            dictCourse['courseName'] = course.name
            dictCourse['courseAbbreviation'] = course.abbreviation
            dictCourse['courseCode'] = course.courseCode
            dictCourse['idCourse'] = course.idCourse
            if course.idCourse in firstIdCourses: #if it is an empty list no one will be at the top
                finalList.insert(0,dictCourse)
                dictCourse['oneOfTheFirst'] = True
            else:
                finalList.append(dictCourse)
                dictCourse['oneOfTheFirst'] = False
        return finalList

    @staticmethod
    def expandCourse(idCourse, idTimePeriod):
        """
         Returns a list of dicts containig the keys: courseName, courseAbbreviation,
         courseCode. Where each one is a possible subgroup of the given course. It could
         be only the practical offers, only the offers given by one professor ...

        @param int idCourse : The database assossiated key to the wanted course
        @param int idTimePeriod : The idTimePeriod of the wanted subgroup's timePeriod.
        @return {} :
        @author
        """
        course = Course.pickById(idCourse)
        offers = Offer.find(course = course, timePeriod = TimePeriod.pickById(idTimePeriod))
        subgroups = Offer.possibleNames(offers)
        finalList = []
        for subgroup in subgroups:
            subgroupDict = {}
            subgroupDict['courseName'] = course.name + subgroup['name']
            subgroupDict['courseAbbreviation'] = course.abbreviation + subgroup['name']
            subgroupDict['courseCode'] = course.courseCode + subgroup['name']
            subgroupDict['idCourse'] = course.idCourse
            finalList.append(subgroupDict)
        return finalList

    @staticmethod
    def getOffers(courseCode, idTimePeriod):
        """
         Returns the set of idOffers defined by this courseCode as is defined in expandCourse method.

        @param string courseCode : If it is a normal course this is not used, if this is a subgroup of a course, this courseCode is going to define the offers.Ex PTC3011(P)[ProfName] = only practical offers given by ProfName in course PTC3011.
        @param int idTimePeriod : The idTimePeriod of the wanted offer's timePeriod.
        @return  :
        @author
        """
        professor = None
        practical = None
        if courseCode.find('[') != -1:
            professorName = courseCode.rsplit('[')[1].rsplit(']')[0]
            professor = Professor.find(name_equal = professorName)[0]
            courseCode = courseCode.rsplit('[')[0] + courseCode.rsplit(']')[1]
        if courseCode.find('(') != -1:
            practical = courseCode.rsplit('(')[1].rsplit(')')[0]
            if practical == 'P':
                practical = True
            elif practical == 'T':
                practical = False
            else:
                raise ColumnsControllerError("The parameter given between the '()' must be equal to 'P' or 'T'.")
            courseCode = courseCode.rsplit('(')[0] + courseCode.rsplit(')')[1]

        course = Course.find(courseCode_equal = courseCode, endDate_equal = '0000-00-00')[0]
        timePeriod = TimePeriod.pickById(idTimePeriod)
        if professor and practical != None:
            offers = Offer.find(course = course, practical = practical, professor = professor, timePeriod = timePeriod)
        elif professor:
            offers = Offer.find(course = course, professor = professor, timePeriod = timePeriod)
        elif practical != None:
            offers = Offer.find(course = course, practical = practical, timePeriod = timePeriod)
        else:
            offers = Offer.find(course = course, timePeriod = timePeriod)
        idOffers = [offer.idOffer for offer in offers]
        return idOffers

    @staticmethod
    def getEncodings(idTimePeriod):
        """
         Return a list of dicts with the keys: idOpticalSheet and encodingName. Where
         each one represents a line of the encoding table, that is related with an
         opticalSheet belonging to the given idTimePeriod.

        @return [] :
        @author
        """
        cursor = MySQLConnection()
        encodings = cursor.execute('SELECT encoding.idOpticalSheet, encoding.name FROM encoding JOIN aggr_opticalSheetField ON encoding.idOpticalSheet = aggr_opticalSheetField.idOpticalSheet JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer WHERE aggr_offer.idTimePeriod = ' + str(idTimePeriod) + ' GROUP BY encoding.idOpticalSheet')
        response = []
        for encoding in encodings:
            encodingDict = {}
            encodingDict['idOpticalSheet'] = encoding[0]
            encodingDict['encodingName'] = encoding[1]
            response.append(encodingDict)
        return response

    @staticmethod
    def removeCycleFromOpticalSheet(idCycle, term, idOpticalSheet):
        """
         Delete the relation between a term of a cycle and an opticalSheet.

        @param int idCycle : 
        @param float term : 
        @param int idOpticalSheet : 
        @return  :
        @author
        """
        cursor = MySQLConnection()
        cursor.execute('DELETE FROM rel_cycle_opticalSheet WHERE idCycle = ' + str(idCycle) + ' AND term = ' + str(term) + ' AND idOpticalSheet = ' + str(idOpticalSheet))
        return


