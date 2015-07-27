from Course import Course   
from tools.MySQLConnection import MySQLConnection
from tools.timeCheck import checkDateString


class IdealTermCourseError(Exception):
    """
     Exception reporting an error in the execution of a Faculty method.

    :version:
    :author:
    """
    pass

class IdealTermCourse(object):

    """
     It is the group of disciplines that belongs to a cycle's term.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idCycle  (private)

     The term (number of the cycle's semester or  quadmester) of the relation.

    term  (private)

     Course that belong to this relation.

    course  (private)

     It says if the course is mandatory, elective or free elective.

    requisitionType  (private)

    startDate  (private)

    endDate  (private)

    """

    def __init__(self, idCycle, term, startDate, requisitionType, course):
        """
         Constructor method.

        @param int idCycle : Associated data base key.
        @param int term : Term of the ideal term.
        @param string startDate : Starting date of this ideal term.
        @param int requisitionType : Type of the requisition of this ideal term.
        @param Course course : The course associated with this ideal term.
        @return  :
        @author
        """
        cursor = MySQLConnection()              
        if not cursor.execute('SELECT idCycle FROM cycle WHERE idCycle = ' + str(idCycle)):   
            raise IdealTermCourseError('idCycle must be in the database')
        if not startDate or not isinstance(startDate,(str,unicode)) or not checkDateString(startDate):
            raise IdealTermCourseError('Must provide a valid start date string in unicode')
        if not requisitionType or not isinstance(requisitionType,(int, long)):
            raise IdealTermCourseError('Must provide a valid requisition type integer')
        if not isinstance(course, Course) or Course.pickById(course.idCourse) != course:
            raise IdealTermCourseError('Must provide a valid course from the database')
        self.idCycle = idCycle
        self.term = term
        self.course = course
        self.requisitionType = requisitionType
        self.startDate = startDate
        self.setEndDate('0000-00-00')

    def setEndDate(self, endDate):
        """
         Set the endDate of this IdealTermCourse.

        @param string endDate : String representing this IdealTermCourse's end date .
        @author
        """
        if not isinstance(endDate, (str,unicode)) or not checkDateString(endDate):
            raise IdealTermCourseError('endDate parameter must be a valid string representing a date')
        self.endDate = endDate


    @staticmethod 
    def find(**kwargs):
        """
         Searches the database to find one or more objects that fit the description
         specified by the method's parameters. It is possible to perform two kinds of
         search when passing a string as a parameter: a search for the exact string
         (EQUAL operator) and a search for at least part of the string (LIKE operator).
         
         Returns:
         All the objects that are related to existing offers in the database, if there
         are not any parameters passed.
         
         A list of objects that match the specifications made by one (or more) of the
         following parameters:
         > idCycle
         > term
         > idCourse
         > requisitionType
         > startDate_equal or startDate_like
         > endDate_equal or endDate_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E.g. IdealTermCourse.find(course = courseObject, term = 3, startDate_equal =
         "2008-10-20", endDate_like = "2010")

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return idealTermCourse[] :
        @author
        """
        cursor = MySQLConnection()
        searchData = cursor.find('SELECT idCourse, idCycle, startDate, endDate, term, requisitionType FROM rel_course_cycle ', kwargs)
        idealTerms = []
        for idealTermData in searchData:
            newIdealTerm = IdealTermCourse(idealTermData[1], idealTermData[4], idealTermData[2].isoformat(), idealTermData[5], Course.pickById(idealTermData[0]))
            if idealTermData[3]:
                newIdealTerm.setEndDate(idealTermData[3].isoformat())
            idealTerms.append(newIdealTerm)
        return idealTerms

    def store(self):
        """
         Creates or alters rel_course_cycle in the database and returns True if it
         works, and False if it does not work.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        if not self.idCycle or not self.course.idCourse or not self.endDate or not self.startDate or not self.term:
            return False
        idCycle = str(self.idCycle)
        idCourse = str(self.course.idCourse)
        term = str(self.term)
        if self.requisitionType:
            requisitionType = str(self.requisitionType)
        else:
            requisitionType = 'NULL'
        querySelect = 'SELECT idCourse, idCycle, startDate, endDate, term, requisitionType FROM rel_course_cycle WHERE idCourse = ' + idCourse + ' and idCycle = ' + idCycle + " and startDate = '" + self.startDate + "' and term = " + term + ' and requisitionType = ' + requisitionType
        queryInsert = 'INSERT INTO rel_course_cycle (idCourse, idCycle, startDate, endDate, term, requisitionType) values (' + idCourse + ', ' + idCycle + ", '" + self.startDate + "', '" + self.endDate + "', " + term + ', ' + requisitionType + ')'
        queryUpdate = "UPDATE rel_course_cycle SET endDate = '" + self.endDate + "' WHERE idCourse = " + idCourse + ' and idCycle = ' + idCycle + " and startDate = '" + self.startDate + "'" + ' and term = ' + term + ' and requisitionType = ' + requisitionType
        try:
            searchData = cursor.execute(querySelect)
            if not searchData:
                cursor.execute(queryInsert)
            else:
                if len(searchData) > 1:
                    raise IdealTermCourseError('More than one object found in query')
                print queryUpdate
                cursor.execute(queryUpdate)
        except:
            return False
        return True
    

    def __eq__(self, other):
        if not isinstance(other, IdealTermCourse):
            return False
        return self.__dict__ == other.__dict__

    def delete(self):
        """
         Deletes the ideal term's data in the data base.
         
         Return: true if successful or false otherwise

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        if not self.course.idCourse or not self.idCycle or not self.endDate:
            raise IdealTermCourseError("Can't uniquely identify object, can't delete database tuple")
            return False
        query = 'DELETE FROM rel_course_cycle WHERE idCourse = ' + str(self.course.idCourse) + ' and idCycle = ' + str(self.idCycle) + " and endDate = '" + self.endDate + "'"
        print query
        try:
            cursor.execute(query)
        except:
            raise IdealTermCourseError("Couldn't delete object")
            return False
        return True

