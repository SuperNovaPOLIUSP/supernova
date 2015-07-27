from pulsarInterface.CourseCoordination import CourseCoordination
from tools.MySQLConnection import MySQLConnection


class FacultyError(Exception):
    """
     Exception reporting an error in the execution of a Faculty method.

    :version:
    :author:
    """
    pass


class Faculty(object):

    """
     


    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated data base key.

    idFaculty  (public)

     Faculty's name

    name  (public)

     The faculty's abbreviation.

    abbreviation  (public)

     Faculty's campus.

    campus  (public)

     Faculty's city.

    city  (public)

    """

    def __init__(self, name, abbreviation):
        """
         Only the name and the abbreviation are needed.

        @param string name : Faculty's name
        @param string abbreviation : Faculty's abbreviation.
        @return  :
        @author
        """
        if not isinstance(name,(str, unicode)):
            raise FacultyError("Parameter name must be a string or an unicode")
        if not isinstance(abbreviation, (str, unicode)):
            raise FacultyError("Parameter abbreviation must be a string or an unicode")
        self.name = name
        self.abbreviation = abbreviation
        self.campus = None
        self.city = None
        self.courseCoordinations = []
        self.idFaculty = None
  
    def __eq__(self, other):
        if not isinstance(other, Faculty):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)
 
    def setCampus(self, campus):
        """
         Set the campus of the faculty, campus can be a string, an unicode or None

        @param string campus : Campus where the faculty is.
        @return  :
        @author
        """
        if campus != None and not isinstance(campus,(str, unicode)):
            raise FacultyError("Parameter campus must be a string or an unicode")
        self.campus = campus

    def setCity(self, city):
        """
         Set the city of the faculty, campus can be a string, an unicode or None

        @param string city : City where the faculty is.
        @return  :
        @author
        """
        if city != None and not isinstance(city,(str, unicode)):
            raise FacultyError("Parameter city must be a string or an unicode")
        self.city = city
 
    def addCourseCoordination(self, courseCoordination):
        """
         Adds a CourseCoordination to the list CourseCoordinations.

        @param CourseCoordination : CourseCoordination to be added to this faculty
        @return bool :
        @author
        """

        if not isinstance(courseCoordination, CourseCoordination) or not CourseCoordination.pickById(courseCoordination.idCourseCoordination) == courseCoordination or courseCoordination in self.courseCoordinations: 
            raise FacultyError('Parameter CourseCoordination must be a CourseCoordination object that exists in the database and does not exist in courseCoordinations.')
         
        self.courseCoordinations.append(courseCoordination)

    def removeCourseCoordination(self, courseCoordination):
        """
         Removes a CourseCoordination from the list courseCoordinations.
         
        @param CourseCoordination: The CourseCoordination to be removed.
        @return bool :
        @author
        """

        if not courseCoordination in self.courseCoordinations: #if the CourseCoordination is in courseCoordination, surely it will be a CourseCoordination object that exists in the database
            raise FacultyError('Parameter courseCoordination must be a courseCoordination object that exists in the list of courseCoordinations of the Faculty.')
    
        self.courseCoordinations.remove(courseCoordination)       
    
    def fillCourseCoordinations(self):
        """
         Finds the courseCoordinations associated to this Faculty through a query in the database.

        @param  :
        @return  :
        @author
        """
        if self.idFaculty != None:
            cursor = MySQLConnection()
            courseCoordinationsData = cursor.execute('SELECT idCourseCoordination FROM rel_courseCoordination_faculty WHERE idFaculty = ' + str(self.idFaculty))
            for courseCoordinationData in courseCoordinationsData:
                self.courseCoordinations.append(CourseCoordination.pickById(courseCoordinationData[0]))
        else:
            raise FacultyError ('idFaculty is not defined')

    @staticmethod
    def pickById(idFaculty):
        """
         Returns a single complete Faculty with the chosen ID.

        @param int idFaculty : Associated data base key.
        @return Faculty :
        @author
        """
        if not isinstance(idFaculty,(int, long)):
            raise FacultyError("Parameter idFaculty must be an integer or a long")

        cursor = MySQLConnection()
        try:
            #If courseData is None or an empty list the [0] at the end will raise an error that will fall to returning None
            facultyData = cursor.execute('SELECT name,abbreviation,campus,city,idFaculty FROM faculty WHERE idFaculty = ' + str(idFaculty))[0]
        except:
            return None
        faculty = Faculty(facultyData[0], facultyData[1])
        faculty.idFaculty = facultyData[4]
        faculty.setCampus(facultyData[2])
        faculty.setCity(facultyData[3])
        faculty.fillCourseCoordinations()        
        return faculty

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
         > idFaculty
         > name_equal or name_like
         > abbreviation_equal or abbreviation_like
         > campus_equal or campus_like
         > courseCoordinations
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. faculty.find(name_equal = "Faculty of Engineering", campus_like = "Main")

        @param dictionary _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        #first prepare the kwargs for the MySQLConnection.find function
        complement = ''
        parameters = {}
        for key in kwargs:
            if key == 'courseCoordinations':      
                complement = ' JOIN rel_courseCoordination_faculty rcf ON rcf.idFaculty = faculty.idFaculty'
                parameters['rcf.idCourseCoordination'] = [courseCoordination.idCourseCoordination for courseCoordination in kwargs['courseCoordinations']]
            else:
                parameters['faculty.' + key] = kwargs[key]
        facultiesData = cursor.find('SELECT faculty.name, faculty.abbreviation, faculty.campus, faculty.city, faculty.idFaculty FROM faculty' + complement ,parameters)
        faculties = []
        for facultyData in facultiesData:
            faculty = Faculty(facultyData[0], facultyData[1])
            faculty.setCampus(facultyData[2])
            faculty.setCity(facultyData[3])
            faculty.idFaculty = facultyData[4]
            faculty.fillCourseCoordinations() 
            faculties.append(faculty)
        return faculties

    def store(self):
        """
         Creates or changes the faculty's data in the data base.
         
        @return :
        @author
        """
        if self.campus == None:
            MySQLcampus = 'NULL' #MySQL None is NULL
        else:
            MySQLcampus = '"' + self.campus + '"'
        if self.city == None:
            MySQLcity = 'NULL'
        else:
            MySQLcity = '"' + self.city + '"'

        cursor = MySQLConnection()
        if self.idFaculty == None:
            #Search for idFaculty
            possibleIds = self.find(name_equal = self.name, abbreviation_equal = self.abbreviation, city_equal = self.city, campus_equal = self.campus)
            if len(possibleIds) > 0:
                self.idFaculty = possibleIds[0].idFaculty   #Since all results are the same faculty pick the first one.
                 
            else:
                #If there is no idFaculty create row
                query = 'INSERT INTO faculty (name, abbreviation, city, campus) VALUES("' + self.name + '", "' + self.abbreviation + '", ' + MySQLcity + ', ' + MySQLcampus + ')'
                cursor.execute(query)
                self.idFaculty = self.find(name_equal = self.name, abbreviation_equal = self.abbreviation, city_equal = self.city, campus_equal = self.campus)[0].idFaculty
                
        else:
            #If there is an idFaculty try to update row
            query = 'UPDATE faculty SET city = ' + MySQLcity + ', campus = ' + MySQLcampus + ' WHERE idFaculty = ' + str(self.idFaculty)
            cursor.execute(query)
        #Storing the courseCoordinations of this Faculty
        cursor.execute('DELETE FROM rel_courseCoordination_faculty WHERE idFaculty = ' + str(self.idFaculty))
        for courseCoordination in self.courseCoordinations:
            query = 'INSERT INTO rel_courseCoordination_faculty (idCourseCoordination, idFaculty) VALUES (' + str(courseCoordination.idCourseCoordination) + ', ' + str(self.idFaculty) + ')'
            cursor.execute(query)

    def delete(self):
        """
         Deletes the faculty's data in the data base.
         
         
        @return :
        @author
        """
        if self.idFaculty != None:
            cursor = MySQLConnection()
            if self == Faculty.pickById(self.idFaculty):
                cursor.execute('DELETE FROM rel_courseCoordination_faculty WHERE idFaculty = ' + str(self.idFaculty))
                cursor.execute('DELETE FROM faculty WHERE idFaculty = ' + str(self.idFaculty))
                return True
            else:
                raise FacultyError("Can't delete non saved object.")
        else:
            raise FacultyError("No idFaculty defined")

   
