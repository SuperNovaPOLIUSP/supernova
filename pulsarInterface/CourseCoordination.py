#encoding: utf8
from pulsarInterface.Cycle import Cycle
from tools.MySQLConnection import MySQLConnection


class CourseCoordinationError(Exception):
    """
     Exception reporting an error in the execution of a CourseCoordination method.

    :version:
    :author:
    """
    pass

class CourseCoordination(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idCourseCoordination  (private)

     CourseCoordination's name.

    name  (public)

     CourseCoordination's abbreviation.

    abbreviation  (public)

    cycles (public)

     List of cycle objects

    """

    def __init__(self, name, abbreviation):
        """
         Constructor method.

        @param string name : CourseCoordination's name
        @param string abbreviation : CourseCoordination's abbreviation
        @return  :
        @author
        """
        #Parameters verificarion.
        if not isinstance(name, (str, unicode)):
            raise CourseCoordinationError('Parameter name must be a string.')
        if not isinstance(abbreviation, (str, unicode)):
            raise CourseCoordinationError('Parameter abbreviation must be a string.')
          
        #Setting other parameters.
        self.name = name
        self.abbreviation = abbreviation
        self.cycles = []
        self.idCourseCoordination = None


    def __eq__(self, other):
        if not isinstance(other, CourseCoordination):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)

    def addCycle(self, cycle):
        """
         Adds a cycle to the list cycles.

        @param Cycle cycle : Cycle to be added to this academic program
        @return bool :
        @author
        """

        if not isinstance(cycle, Cycle) or not Cycle.pickById(cycle.idCycle) == cycle or cycle in self.cycles: 
            raise CourseCoordinationError('Parameter cycle must be a cycle object that exists in the database and does not exist in cycles.')
    
        self.cycles.append(cycle)
        
    def removeCycle(self, cycle):
        """
         Removes a cycle from the list cycles.
         
        @param Cycle cycle : The cycle to be removed.
        @return bool :
        @author
        """

        if not cycle in self.cycles: #if the cycle is in cycles, surely it will be a Cycle object that exists in the database
            raise CourseCoordinationError('Parameter cycle must be a Cycle object that exists in the list of cycles of the AcademicProgram.')
    
        self.cycles.remove(cycle)       
    
    def fillCycles(self):
        """
         Finds the cycles associated to this Faculty through a query in the database.

        @param  :
        @return  :
        @author
        """
        if self.idCourseCoordination != None:
            cursor = MySQLConnection()
            cyclesData = cursor.execute('SELECT idCycle FROM rel_courseCoordination_cycle WHERE idCourseCoordination = ' + str(self.idCourseCoordination))
            for cycleData in cyclesData:
                self.cycles.append(Cycle.pickById(cycleData[0]))
        else:
            raise CourseCoordinationError ('idCourseCoordination is not defined')

    @staticmethod
    def pickById(idCourseCoordination):
        """
         Returns a CourseCoordination object with the chosen idCourseCoordination.

        @param int idCourseCoordination : Associated database key.
        @return CourseCoordination :
        @author
        """
        cursor = MySQLConnection()
        query = 'SELECT idCourseCoordination, name, abbreviation FROM courseCoordination WHERE idCourseCoordination = ' + str(idCourseCoordination)
        try:
            courseCoordinationData = cursor.execute(query)[0]
        except:
            return None
        courseCoordination = CourseCoordination(courseCoordinationData[1], courseCoordinationData[2])
        courseCoordination.idCourseCoordination = courseCoordinationData[0]
        courseCoordination.fillCycles()
        return courseCoordination
        
    @staticmethod
    def find( **kwargs):
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
         > idCourseCoordination
         > name_equal or name_like
         > abbreviation_equal or abbreviation_like
         > cycles
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. CourseCoordination.find(name_equal = "Coc Civil")

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        #first prepare the kwargs for the MySQLConnection.find function
        complement = ''
        parameters = {}
        for key in kwargs:
            if key == 'cycles':      
                complement = ' JOIN rel_courseCoordination_cycle rcc ON rcc.idCourseCoordination = courseCoordination.idCourseCoordination'
                parameters['rcc.idCycle'] = [cycle.idCycle for cycle in kwargs['cycles']]
            else:
                parameters['courseCoordination.' + key] = kwargs[key]
        courseCoordinationsData = cursor.find('SELECT courseCoordination.idCourseCoordination, courseCoordination.name, courseCoordination.abbreviation FROM courseCoordination' + complement, parameters)
        courseCoordinations = []
        for courseCoordinationData in courseCoordinationsData:         
            courseCoordination = CourseCoordination(courseCoordinationData[1], courseCoordinationData[2])
            courseCoordination.idCourseCoordination = courseCoordinationData[0]
            courseCoordination.fillCycles()
            courseCoordinations.append(courseCoordination)
        return courseCoordinations

    def store(self):
        """
         Creates or alters an CourseCoordination in the database.

        @return bool :
        @author
        """

        cursor = MySQLConnection()
        if self.idCourseCoordination == None:
            courseCoordinations = CourseCoordination.find(name_equal = self.name, abbreviation_equal = self.abbreviation)
            if len(courseCoordinations) > 0:
                self.idCourseCoordination = courseCoordinations[0].idCourseCoordination #Any courseCoordination that fit those paramaters is the same as this courseCoordination, so no need to save
                
            else:
                #Create this department
                query = 'INSERT INTO courseCoordination (name, abbreviation) VALUES("' + self.name + '", "' + self.abbreviation + '")'
                cursor.execute(query)
                self.idCourseCoordination = CourseCoordination.find(name_equal = self.name, abbreviation_equal = self.abbreviation)[0].idCourseCoordination   
  
        #Storing the cycles of this courseCoordinations
        cursor.execute('DELETE FROM rel_courseCoordination_cycle WHERE idCourseCoordination = ' + str(self.idCourseCoordination))
        for cycle in self.cycles:
            query = 'INSERT INTO rel_courseCoordination_cycle (idCourseCoordination, idCycle) VALUES (' + str(self.idCourseCoordination) + ', ' + str(cycle.idCycle) + ')'
            cursor.execute(query)


    def delete(self):
        """
         Deletes the CourseCoordination's data in the data base.
        
        @return bool :
        @author
        """
        if self.idCourseCoordination != None:
            cursor = MySQLConnection()
            if self == CourseCoordination.pickById(self.idCourseCoordination):
                cursor.execute('DELETE FROM rel_courseCoordination_cycle WHERE idCourseCoordination = ' + str(self.idCourseCoordination))           
                cursor.execute('DELETE FROM rel_courseCoordination_faculty WHERE idCourseCoordination = ' + str(self.idCourseCoordination))
                cursor.execute('DELETE FROM courseCoordination WHERE idCourseCoordination = ' + str(self.idCourseCoordination))
            else:
                raise CourseCoordinationError("Can't delete non saved object.")
        else:
            raise CourseCoordinationError('No idCourseCoordination defined.')




