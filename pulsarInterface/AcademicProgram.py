#encoding: utf8
import datetime

from pulsarInterface.Cycle import Cycle
from tools.MySQLConnection import MySQLConnection
from tools.timeCheck import checkDateString


class AcademicProgramError(Exception):
    """
     Exception reporting an error in the execution of a AcademicProgram method.

    :version:
    :author:
    """
    pass

class AcademicProgram(object):

    """
     Representation of an AcademicProgram in the data base.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idAcademicProgram  (public)

     Academic program's name.

    name  (public)

     Vacancies's number in this academic program.

    vacancyNumber  (public)

     Academic program's abbreviation.

    abbreviation  (public)

     Date of start of this academic program, in the form year-month-day ''xxxx-xx-xx''.
     Start is defined as the start of the academic program in general, not only in
     this year, but the first time it was in this University.

    startDate  (public)

     Date of end of this academic program, in the form year-month-day ''xxxx-xx-xx''.
     end is defined as the end of the academic program in general.

    endDate  (public)

     List of objects Cycle belonging to this Academic Program.

    cycles  (public)

    """

    def __init__(self, name, abbreviation, startDate):
        """
         Constructor method.

        @param string name : Academic program's name.
        @param string abbreviation : Academic program's abbreviation.
        @param string startDate : The start date of this academic program
        @return  :
        @author
        """

        #Parameters verification.
        if not isinstance(name, (str, unicode)):
            raise AcademicProgramError('Parameter name must be a string.')
        if not isinstance(abbreviation, (str, unicode)):
            raise AcademicProgramError('Parameter abbreviation must be a string.')
        if not isinstance(startDate, datetime.date):
            if not isinstance (startDate, (str, unicode)) or not checkDateString(startDate) : 
                raise AcademicProgramError('Parameter startDate must be a date.')
            
        #Setting other parameters.
        self.name = name
        self.abbreviation = abbreviation
        self.startDate = str(startDate)
        #Setting None parameters.
        self.idAcademicProgram = None
        self.cycles = []
        self.vacancyNumber = None
        self.endDate = None

    def __eq__(self, other):
        if not isinstance(other, AcademicProgram):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)


    def setVacancyNumber(self, vacancyNumber):
        """
         Sets the number of vacancies in the academic program.

        @param int vacancyNumber : Vacancies's number in this academic program.
        @return  :
        @author
        """
        
        if not isinstance(vacancyNumber, (int, long)) and vacancyNumber != None:
            raise AcademicProgramError('Parameter vacancyNumber must be an int or a long.')

        self.vacancyNumber = vacancyNumber


    def setEndDate(self, endDate):
        """
         Set the endDate of this academic program.

        @param string endDate : End date of this academic program.
        @return  :
        @author
        """
        if endDate != None:
            if not isinstance(endDate, datetime.date):
                if not isinstance (endDate, (str, unicode)) or not checkDateString(endDate) : 
                    raise AcademicProgramError('Parameter endDate must be a date.')
   
            self.endDate = str(endDate)
        else:
            self.endDate = endDate

    def addCycle(self, cycle):
        """
         Adds a Cycle to the list cycles.

        @param Cycle Cycle : Cycle to be added to this academic program
        @return bool :
        @author
        """

        if not isinstance(cycle, Cycle) or not Cycle.pickById(cycle.idCycle) == cycle or cycle in self.cycles: 
            raise AcademicProgramError('Parameter cycle must be a cycle object that exists in the database and does not exist in cycles.')
    
        self.cycles.append(cycle)
        
    def removeCycle(self, cycle):
        """
         Removes a Cycle from the list cycles.
         
        @param Cycle Cycle : The Cycle to be removed.
        @return bool :
        @author
        """

        if not cycle in self.cycles: #if the cycle is in cycles, surely it will be a Cycle object that exists in the database
            raise AcademicProgramError('Parameter cycle must be a cycle object that exists in the list of cycles of the AcademicProgram.')
    
        self.cycles.remove(cycle)       
    
    def fillCycles(self):
        """
         Finds the cycles associated to this AcademicProgram through a query in the database.

        @param  :
        @return  :
        @author
        """
        if self.idAcademicProgram != None:
            cursor = MySQLConnection()
            cyclesData = cursor.execute('SELECT idCycle FROM rel_academicProgram_cycle WHERE idAcademicProgram = ' + str(self.idAcademicProgram))
            for cycleData in cyclesData:
                self.cycles.append(Cycle.pickById(cycleData[0]))
        else:
            raise AcademicProgramError ('idAcademicProgram is not defined')

    @staticmethod
    def pickById(idAcademicProgram):
        """
         Returns an AcademicProgram object with the chosen idAcademicProgram.

        @param int idAcademicProgram : Associated database key.
        @return AcademicProgram :
        @author
        """
        cursor = MySQLConnection()
        query = 'SELECT idAcademicProgram, name, vacancyNumber, abbreviation, startDate, endDate FROM academicProgram WHERE idAcademicProgram = ' + str(idAcademicProgram)
        academicProgramData = cursor.execute(query)[0]
        try:
            academicProgramData = cursor.execute(query)[0]
        except:
            return None
        academicProgram = AcademicProgram(academicProgramData[1], academicProgramData[3], academicProgramData[4])
        academicProgram.setVacancyNumber(academicProgramData[2])
        academicProgram.setEndDate(academicProgramData[5])
        academicProgram.idAcademicProgram = academicProgramData[0]
        academicProgram.fillCycles()
        return academicProgram
        
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
         > idAcademicProgram
         > name_equal or name_like
         > abbreviation_equal or abbreviation_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. AcademicProgram.find(name_equal = "Computing Science")

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        
        cursor = MySQLConnection()
        #first prepare the kwargs for the MySQLConnection.find function
        complement = ''
        parameters = {}
        for key in kwargs:
            if key == 'cycles':      
                complement = ' JOIN rel_academicProgram_cycle rac ON rac.idAcademicProgram = academicProgram.idAcademicProgram'
                parameters['rac.idCycle'] = [cycle.idCycle for cycle in kwargs['cycles']]
            else:
                parameters['academicProgram.' + key] = kwargs[key]
        academicProgramsData = cursor.find('SELECT academicProgram.name, academicProgram.vacancyNumber, academicProgram.abbreviation, academicProgram.startDate, academicProgram.idAcademicProgram, academicProgram.endDate FROM academicProgram' + complement ,parameters)
        academicPrograms = []
        for academicProgramData in academicProgramsData:         
            academicProgram = AcademicProgram(academicProgramData[0], academicProgramData[2], academicProgramData[3])
            academicProgram.setVacancyNumber(academicProgramData[1])
            academicProgram.setEndDate(academicProgramData[5])
            academicProgram.idAcademicProgram = academicProgramData[4]
            academicProgram.fillCycles()
            academicPrograms.append(academicProgram)
        return academicPrograms

    def store(self):
        """
         Creates or alters an AcademicProgram in the database.

        @return bool :
        @author
        """

        cursor = MySQLConnection()
        if self.vacancyNumber == None:
            mySQLVacancyNumber = 'NULL'  #in MySQL is NULL
        else:
            mySQLVacancyNumber = self.vacancyNumber

        if self.endDate == None:
            mySQLEndDate = 'NULL'  #in MySQL is NULL
        else:
            mySQLEndDate = '"' + self.endDate + '"'
        
        if self.idAcademicProgram == None:
            academicPrograms = self.find(name_equal = self.name, vacancyNumber = self.vacancyNumber, abbreviation_equal = self.abbreviation, startDate_equal = self.startDate, endDate_equal = self.endDate)
            if len(academicPrograms) > 0:
                self.idAcademicProgram = academicPrograms[0].idAcademicProgram #Any offer that fit those parameters is the same as this offer
                
            else: 
                #If there is no idAcademicProgram create row
                query = 'INSERT INTO academicProgram (name, vacancyNumber, abbreviation, startDate, endDate) VALUES("' + self.name + '", ' + str(mySQLVacancyNumber) + ', "' + self.abbreviation + '", "' + str(self.startDate) + '", ' + mySQLEndDate + ')'
                cursor.execute(query)
                self.idAcademicProgram = AcademicProgram.find(name_equal = self.name, vacancyNumber = self.vacancyNumber, abbreviation_equal = self.abbreviation, startDate_equal = self.startDate, endDate_equal = self.endDate)[0].idAcademicProgram
        else:
            #Update offer
            query = 'UPDATE academicProgram SET vacancyNumber = ' + str(mySQLVacancyNumber) + ', endDate = ' + mySQLEndDate + ' WHERE idAcademicProgram = ' + str(self.idAcademicProgram) 
            cursor.execute(query)
      
        for cycle in self.cycles:
            query = 'INSERT INTO rel_academicProgram_cycle (idAcademicProgram, idCycle) VALUES(' + str(self.idAcademicProgram) + ', ' + str(cycle.idCycle) + ')'
            cursor.execute(query)     
        return

    def delete(self):
        """
         Deletes the academicProgram's data in the data base.
        
        @return bool :
        @author
        """
        if self.idAcademicProgram != None:
            cursor = MySQLConnection()
            if self == AcademicProgram.pickById(self.idAcademicProgram):
                cursor.execute('DELETE FROM rel_academicProgram_cycle WHERE idAcademicProgram = ' + str(self.idAcademicProgram))           
                cursor.execute('DELETE FROM academicProgram WHERE idAcademicProgram = ' + str(self.idAcademicProgram))
            else:
                raise AcademicProgramError("Can't delete non saved object.")
        else:
            raise AcademicProgramError('No idAcademicProgram defined.')




