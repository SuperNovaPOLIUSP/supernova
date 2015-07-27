#coding: utf8

import datetime

from tools.MySQLConnection import MySQLConnection
from tools.timeCheck import checkDateString


class CourseError(Exception):
    """
     Exception reporting an error in the execution of a Course method.

    :version:
    :author:
    """
    pass

class Course(object):

    """
     Representation of a course in the database.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idCourse  (public)

     7 character code that represents the course.

    courseCode  (public)

     Abbreviation of the course's name.

    abbreviation  (public)

     Complete name of a course

    name  (public)

    
    Date of start of this course, in the form year-month-day “xxxx-xx-xx”. Start is 
    defined as the start of the course in general, not only in this year, but the 
    first time it was in this University. 

    startDate  (public)

     Date of the end of this course, in the form year-month-day "xxxx-xx-xx". It's
     value is null if the course is not over. Over is defined as the last time this
     discipline is given was this University

    endDate  (public)

    """

    def __init__(self, courseCode, name, startDate):
        """
         A course is defined by a name and a 7 character code.

        @param string courseCode : A 7 character code that represents the course.
        @param string name : Complete name of a discipline.
        @return  :
        @author
        """
        if not isinstance(courseCode,(str,unicode)):
            raise CourseError('Parameter courseCode must be a string or an unicode')
        if not isinstance(name,(str,unicode)):
            raise CourseError('Parameter name must be a string or an unicode')
        if not isinstance(startDate,datetime.date):
            if not isinstance(startDate,(str,unicode)) or checkDateString(startDate) == None:
                raise CourseError('Parameter startDate must be a datetime.date format or a string in the format year-month-day')

        self.startDate = str(startDate)
        self.courseCode = courseCode
        self.name = name
        self.abbreviation = name #By default abbreviation is equal to name
        self.idCourse = None
        self.endDate = None

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other) 

    def setAbbreviation(self, abbreviation):
        """
         Set the abbreviation of this course.

        @param string abbreviation : Abbreviation of the course's name.
        @return string :
        @author
        """
        if not isinstance(abbreviation,(str,unicode)):
            raise CourseError("Parameter abbreviation must be str or unicode")
        self.abbreviation = abbreviation

    def setEndDate(self, endDate):
        """
         Set the endDate of this course .

        @param string endDate : String defining the end  date of this course, in the form year-month-day "xxxx-xx-xx".
        @return string :
        @author
        """
        if endDate != None:
            if not isinstance(endDate,datetime.date):
                if not isinstance(endDate,(str,unicode)) or checkDateString(endDate) == None:
                    raise CourseError('Parameter endDate must be a datetime.date format or a string in the format year-month-day')
            self.endDate = str(endDate)
        else:
            self.endDate = endDate

    @staticmethod
    def pickById(idCourse):
        """
         Returns a single course with the chosen ID.

        @param int idCourse : Associated data base key.
        @return int :
        @author
        """
        cursor = MySQLConnection()
        try:
            #If courseData is None or an empty list the [0] at the end will raise an error that will fall to returning None
            courseData = cursor.execute('SELECT idCourse, courseCode, abbreviation, name, startDate, endDate FROM course WHERE idCourse = ' + str(idCourse))[0]
        except:
            return None

        course = Course(courseData[1],courseData[3],str(courseData[4]))
        course.idCourse = courseData[0]
        course.setAbbreviation(courseData[2])
        course.setEndDate(courseData[5]) 
        return course        

    @staticmethod
    def find(**kwargs):
        """
         Searches the database to find one or more objects that fit the description
         specified by the method's parameters. It is possible to perform two kinds of
         search when passing a string as a parameter: a search for the exact string
         (EQUAL operator) and a search for at least part of the string (LIKE operator).
         
         Returns:
         All the objects that are related to existing course in the database, if there
         are not any parameters passed.
         
         A list of objects that match the specifications made by one (or more) of the
         following parameters:
         > idCourse
         > courseCode_equal or courseCode_like
         > abbreviation_equal or abbreviation_like
         > name_equal or name_like
         > startDate_equal or startDate_like
         > endDate_equal or endDate_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Course.find(name_like = "Computer", courseCode_equal = "MAC2166")

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return course[] : 
        @author
        """
        cursor = MySQLConnection()
        coursesData = cursor.find('SELECT idCourse, courseCode, abbreviation, name, startDate, endDate FROM course',kwargs)
        courses = []
        for courseData in coursesData:
            course = Course(courseData[1],courseData[3], str(courseData[4]))
            course.idCourse = courseData[0]
            course.setAbbreviation(courseData[2])
            course.setEndDate(courseData[5]) 
            courses.append(course)
        return courses

    def store(self):
        """
         Creates or alters a course in the database.
        @return :
        @author
        """
        cursor = MySQLConnection()
        if self.endDate == None:
            mySQLEndDate = '"0000-00-00"'  #in MySQL is NULL
        else:
            mySQLEndDate = '"' + self.endDate + '"'
        if self.idCourse == None:
            courses = Course.find(courseCode_equal = self.courseCode, abbreviation_equal = self.abbreviation, name_equal = self.name, startDate_equal = str(self.startDate), endDate_equal = self.endDate)
            if len(courses) > 0:
                self.idCourse = courses[0].idCourse #Any course that fit those parameters is the same as this course, so no need to save
                return
            else: 
                #Create this course
                query = 'INSERT INTO course (courseCode, abbreviation, name, startDate, endDate) VALUES("' + self.courseCode + '", "' + self.abbreviation + '", "' + self.name + '", "' + str(self.startDate) + '", ' + mySQLEndDate + ')'
                cursor.execute(query)
                self.idCourse = Course.find(courseCode_equal = self.courseCode, abbreviation_equal = self.abbreviation, name_equal = self.name, startDate_equal = str(self.startDate), endDate_equal = self.endDate)[0].idCourse 
        else:
            #Update Course
            query = 'UPDATE course SET abbreviation = "' + self.abbreviation + '", endDate = ' + mySQLEndDate + ' WHERE idCourse = ' + str(self.idCourse)
            cursor.execute(query)
        return

    def delete(self):
        """
         Deletes the course's data in the database.
         

        @return :
        @author
        """
        if self.idCourse != None:
            cursor = MySQLConnection()
            if self == Course.pickById(self.idCourse):
                cursor.execute('DELETE FROM course WHERE idCourse = ' + str(self.idCourse))
                cursor.execute('DELETE FROM rel_course_cycle WHERE idCourse = ' + str(self.idCourse))
                cursor.execute('DELETE FROM rel_course_cycle_course WHERE idCourse = ' + str(self.idCourse) + ' or idRequirement = ' + str(self.idCourse))        
            else:
                raise CourseError("Can't delete non saved object.")
        else:
            raise CourseError('idCourse not defined.')




