# coding: utf-8
import datetime

from pulsarInterface.IdealTermCourse import IdealTermCourse
from tools.MySQLConnection import MySQLConnection
from tools.timeCheck import checkDateString


class CycleError(Exception):
    """
     Exception reporting an error in the execution of a Offer method.

    :version:
    :author:
    """
    pass



class Cycle(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated data base key.

    idCycle  (public)

     Cycle's name.

    name  (public)

     Date of start of this cycle, in the form year-month-day “xxxx-xx-xx”. Start
     is defined as the start of the cycle in this University.

    startDate  (public)

     Date of the end of this cycle, in the form year-month-day “xxxx-xx-xx”.
     Its value is null if the cycle is not over. Over is defined as the last
     time this cycle was given in this University.

    endDate  (public)

     It represents the type of cycle, (e.g general area, basic cycle ...).

    cycleType  (public)

     Cycle Code (as defined by jupiter)

    cycleCode  (public)

     String representing the time period division ("quarter" or "semester")

    termLength  (public)

     List of Idealterm where each one contains a set of mandatory courses of this
     cycle.

    mandatoryIdealTerms  (public)

     List of IdealTermCourse where each one contains a set of elective courses of this
     cycle.

    electiveIdealTerms  (public)

     Abbreviated cycle's name (e.g. Computing Engineering -> Computing).

    abbreviation  (public)

     Number of vacancies for this cycle.

    vacancyNumber  (public)

     Cycle's daily length (day-time, nigth-time,full-time)

    dayPeriod  (public)

    """

    def __init__(self, name, cycleType, cycleCode, termLength, startDate, dayPeriod):
        """

        @param string name : Cycle's name
        @param string cycleType : It represents the type of cycle, (e.g general area, basic cycle,... ).
        @param string cycleCode : codigo da habilitação (vide jupiter)
        @param string termLength : String representing the period division ("quarter" or "semester").
        @param startDate string : Date of the start of this cycle, in the form year-month-day “xxxx-xx-xx”.Start is defined as the first time this cycle was given in this University. 
        @param string dayPeriod : Cycle's daily length (day-time, nigth-time,full-time)
        @return  :
        @author
        """
        if not isinstance(name, (str, unicode)):
            raise CycleError('Parameter name must be a string or unicode.')
        if not isinstance(cycleType, (str, unicode)):
            raise CycleError('Parameter cycleType must be a string or unicode.')            
        if not isinstance(cycleCode, (int, long)):
            raise CycleError('Parameter cycleCode must be an int or a long.')
        if not isinstance(termLength, (str, unicode)):
            raise CycleError('Parameter termLength must be a string or unicode.')
        if not isinstance(startDate,datetime.date):
            if not isinstance(startDate,(str,unicode)) or not checkDateString(startDate):
                raise CycleError('Parameter startDate must be a datetime.date format or a string in the format year-month-day')
        if not isinstance(dayPeriod, (str, unicode)):
            raise CycleError('Parameter dayPeriod must be a string or unicode.')


        self.name = name
        self.cycleType = cycleType
        self.idCycleType = self.getIdCycleType()
        self.cycleCode = cycleCode
        self.termLength = termLength
        self.idTermLength = self.getIdTermLength()
        self.startDate = str(startDate) 
        self.abbreviation = name
        self.dayPeriod = dayPeriod
        self.vacancyNumber = None
        self.idCycle = None
        self.endDate = None
        self.mandatoryIdealTerms = None
        self.electiveIdealTerms = None
        
    def __eq__(self, other):
        if not isinstance(other, Cycle):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)

    def setEndDate(self, endDate):
        """

        @param string endDate : Date of the end of this cycle, in the form year-month-day “xxxx-xx-xx”. It's value is null if the cycle is not over. Over is defined as the last time this cycle was given in this University.
        @return  :
        @author
        """
        if endDate != None:
            if not isinstance(endDate,datetime.date):
                if not isinstance(endDate,(str,unicode)) or not checkDateString(endDate):
                    raise CycleError('Parameter endDate must be a datetime.date format or a string in the format year-month-day')
            self.endDate = str(endDate)
        else:
            self.endDate = endDate

    def setVacancyNumber(self, vacancyNumber):
        """
         

        @param int vancacyNumber : 
        @return  :
        @author
        """
        if vacancyNumber != None:
            if not isinstance(vacancyNumber, (int, long)):
                raise CycleError('Parameter vacancyNumber must be a int or a long.')
        self.vacancyNumber = vacancyNumber
       

    def setAbbreviation(self, abbreviation):
        """
         

        @param string abbreviation : 
        @return  :
        @author
        """
        if not isinstance(abbreviation, (str, unicode)):    
            raise CycleError('Parameter abbreviation must be a string or unicode.')
        self.abbreviation = abbreviation

    def completeMandatoryIdealTerms(self):
        """
         Completes the mandatoryIdealTerms list with the objects idealTermCourse related to the
         mandatories time period of this cycle.

        @return bool :
        @author
        """
        mandatoryIdealTerms = IdealTermCourse.find(idCycle = self.idCycle, requisitionType = 1)
        self.mandatoryIdealTerms = {}
        for mIdealTermCourse in mandatoryIdealTerms:
            if not mIdealTermCourse.term in self.mandatoryIdealTerms.keys():
                self.mandatoryIdealTerms[mIdealTermCourse.term] = []
            self.mandatoryIdealTerms[mIdealTermCourse.term].append(mIdealTermCourse)
        

    def completeElectiveIdealTerms(self):
        """
         Completes the electiveIdealTerms list with the objects idealTermCourse related to the
         electives time period of this cycle.

        @return bool :
        @author
        """
        electiveIdealTerms = IdealTermCourse.find(idCycle = self.idCycle, requisitionType = 2)
        self.electiveIdealTerms = {}
        for eIdealTermCourse in electiveIdealTerms:
            if not eIdealTermCourse.term in self.electiveIdealTerms.keys():
                self.electiveIdealTerms[eIdealTermCourse.term] = []
            self.electiveIdealTerms[eIdealTermCourse.term].append(eIdealTermCourse)
        
    def getIdCycleType(self):
        """
        Once set a Cycle type, returns its Id on the DB.
        Creates one if it does not exist
        """
        cursor = MySQLConnection()
        query = "SELECT idCycleType FROM minitableCycleType WHERE name = '" + self.cycleType + "'"
        idCycleType = cursor.execute(query)
        if len(idCycleType) >0:
            return idCycleType[0][0]
        else:#we have to create it on the DB
            query = "INSERT INTO minitableCycleType (name) VALUES ('" +self.cycleType +"')"
            cursor.execute(query)
            query = "SELECT idCycleType FROM minitableCycleType WHERE name = '" +self.cycleType +"'"
            return cursor.execute(query)[0][0]
            
    def getIdTermLength(self):
        """
        Once set a term length, returns its Id on the DB.
        Creates one if it does not exist
        """
        cursor = MySQLConnection()
        query = "SELECT idLength FROM minitableLength WHERE length = '" + self.termLength + "'"
        idTermLength = cursor.execute(query)
        if len(idTermLength) >0:
            return idTermLength[0][0]
        else:#we have to create it on the DB
            query = "INSERT INTO minitableLength (length) VALUES ('" +self.termLength +"')"
            cursor.execute(query)
            query = "SELECT idLength FROM minitableLength WHERE length = '" +self.termLength +"'"
            return cursor.execute(query)[0][0]

    @staticmethod
    def pickById(idCycle):
        """
         Returns a single cycle with the chosen ID.

        @param int idCycle : Associated data base key.
        @return Cycle :
        @author
        """
        cursor = MySQLConnection()  
        try:
            #Here get most of the cycles data
            cycleData = cursor.execute('SELECT curr.name,  mc.name, curr.cycleCode, curr.startDate, curr.dayPeriod, curr.vacancyNumber, curr.endDate, curr.abbreviation, ml.length  FROM cycle curr JOIN minitableCycleType mc ON curr.idCycleType = mc.idCycleType JOIN minitableLength ml ON ml.idLength = curr.termLength WHERE curr.idCycle = '+ str(idCycle))[0]
        except:
            return None
        
        cycle = Cycle(cycleData[0], cycleData[1], cycleData[2], cycleData[8], cycleData[3], cycleData[4])#name, cycleType, cycleCode, termLength, startDate, dayPeriod
        cycle.setVacancyNumber(cycleData[5])
        cycle.setEndDate(cycleData[6])
        cycle.setAbbreviation(cycleData[7])
        cycle.idCycle = idCycle
        return cycle

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
         > name_equal or name_like
         > startDate_equal or startDate_like
         > endDate_equal or endDate_like
         > cycleType
         > cycleCode
         > termLength_equal or termLength_like
         > abbreviation_equal or abbreviation_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Cycle.find(termLength_equal = "night", name_like = "Computer")

        @param dictionary _kwargs : 
        @return Curriculo[] :
        @author
        """
        cursor = MySQLConnection()
        parameters = {}
        for key in kwargs:
            if key.find('cycleType') != -1:
                if key.find('like') != -1:
                    parameters['mc.name_like'] = kwargs[key]
                else:
                    parameters['mc.name_equal'] = kwargs[key]
            elif key.find('termLength') != -1:
                parameters['ml.length' + key.split('termLength')[1]] = kwargs[key]
            else:
                parameters['curr.' + key] = kwargs[key]
        cyclesData = cursor.find('SELECT curr.idCycle, curr.name,  mc.name, curr.cycleCode, curr.startDate, curr.dayPeriod, curr.vacancyNumber, curr.endDate, curr.abbreviation, ml.length FROM cycle curr JOIN minitableCycleType mc ON curr.idCycleType = mc.idCycleType JOIN minitableLength ml ON ml.idLength = curr.termLength ',parameters)
        cycles = []
        for cycleData in cyclesData:
            cycle = Cycle(cycleData[1], cycleData[2], cycleData[3], cycleData[9], cycleData[4], cycleData[5])#name, cycleType, cycleCode, termLength, startDate, dayPeriod
            cycle.setVacancyNumber(cycleData[6])
            cycle.setEndDate(cycleData[7])
            cycle.setAbbreviation(cycleData[8])
            cycle.idCycle = cycleData[0]
            cycles.append(cycle)
        return cycles
        
        #name, cycleType, cycleCode, termLength, startDate, dayPeriod
    def store(self):
        """
         Alters the cycle's data in the data base.

        @return bool :
        @author
        """     
        if self.idCycle == None:
            cycles = Cycle.find(name_equal = self.name, startDate_equal = self.startDate, endDate_equal = self.endDate, cycleType_equal = self.cycleType, cycleCode = self.cycleCode, termLength_equal = self.termLength, abbreviation_equal = self.abbreviation)
            if len(cycles) > 0:
                self.idCycle = cycles[0].idCycle #Any cycle that fit those parameters is the same as this cycle, so no need to save
                return
            else:
                #Create this cycle
                query = "INSERT INTO cycle (name, idCycleType, cycleCode, startDate, abbreviation"
                values = ") VALUES('" +self.name +"', '" +str(self.idCycleType) +"', '" +str(self.cycleCode) +"', '" +self.startDate +"', '" + self.abbreviation + "'"
                if self.endDate != None:
                    query += ", endDate"
                    values += ", '" +self.endDate + "'"
                if self.termLength != None:
                    query += ", termLength"
                    values += ", " + str(self.idTermLength)
                if self.vacancyNumber != None:
                    query += ", vacancyNumber"
                    values += ", " + str(self.vacancyNumber)
                if self.dayPeriod != None:
                    query += ", dayPeriod"
                    values += ", '" +self.dayPeriod +"'"
                cursor = MySQLConnection()
                cursor.execute(query + values +")")
                self.idCycle = Cycle.find(name_equal = self.name, startDate_equal = self.startDate, endDate_equal = self.endDate, cycleType_equal = self.cycleType, cycleCode = self.cycleCode, termLength_equal = self.termLength, abbreviation_equal = self.abbreviation)[0].idCycle 
        
        else:#we need to update the object in the bank
            #let's find out what needs to be updated
            old = Cycle.pickById(self.idCycle)
            if self == old:
                #nothing to update
                return
            else:
                query = '''UPDATE cycle SET '''
                firstItem = 1
                if self.name != old.name:
                    query += "name = '" +self.name +"'"
                if self.startDate != old.startDate:
                    if firstItem == 0: query += ", "
                    else: firstItem = 0
                    query += "startDate = " +self.startDate
                if self.endDate != old.endDate:
                    if firstItem == 0: query += ", "
                    else: firstItem = 0
                    if self.endDate != None:
                        query += "endDate = '" + self.endDate + "'"
                    else:
                        query += "endDate = NULL"
                if self.cycleType != old.cycleType:
                    if firstItem == 0: query += ", "
                    else: firstItem = 0
                    idCycleType = self.getIdCycleType()
                    query += "idCycleType = " +str(idCycleType)
                if self.cycleCode != old.cycleCode:
                    if firstItem == 0: query += ", "
                    else: firstItem = 0
                    query += "cycleCode = " +str(self.cycleCode)
                if self.idTermLength != old.idTermLength:
                    if firstItem == 0: query += ", "
                    else: firstItem = 0
                    query += "termLength = " + str(self.idTermLength)
                if self.abbreviation != old.abbreviation:
                    if firstItem == 0: query += ", "
                    else: firstItem = 0
                    query += "abbreviation = '" +self.abbreviation +"'"
                if self.vacancyNumber != old.vacancyNumber:
                    if firstItem == 0: query += ", "
                    else: firstItem = 0
                    query += "vacancyNumber = " +str(self.vacancyNumber)
                if self.dayPeriod != old.dayPeriod:
                    if firstItem == 0: query += ", "
                    else: firstItem = 0
                    query += "dayPeriod = '" +self.dayPeriod +"'"
                
                query += ''' WHERE idCycle = ''' +str(self.idCycle)
                cursor = MySQLConnection()
                cursor.execute(query)

    def delete(self):
        """
         Deletes the cycle's data in the data base.
         
         Return: true if successful or false otherwise

        @return bool :
        @author
        """
        
        if self.idCycle != None:
            cursor = MySQLConnection()
            if self == Cycle.pickById(self.idCycle):
                cursor.execute('DELETE FROM rel_course_cycle WHERE idCycle = ' + str(self.idCycle))
                cursor.execute('DELETE FROM rel_courseCoordination_cycle WHERE idCycle = ' + str(self.idCycle))
                cursor.execute('DELETE FROM rel_academicProgram_cycle WHERE idCycle = ' + str(self.idCycle))
                cursor.execute('DELETE FROM rel_course_cycle_course WHERE idCycle = ' + str(self.idCycle))
                cursor.execute('DELETE FROM rel_cycle_opticalSheet WHERE idCycle = ' + str(self.idCycle))
                cursor.execute('DELETE FROM cycle WHERE idCycle = ' + str(self.idCycle))
            else:
                raise CycleError("Can't delete non saved object.")
        else:
            raise CycleError('idCycle not defined.')



