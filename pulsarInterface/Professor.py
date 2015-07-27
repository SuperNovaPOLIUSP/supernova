#encoding: utf8
from pulsarInterface.Department import Department
from tools.MySQLConnection import MySQLConnection


class ProfessorError(Exception):
    """
     Exception reporting an error in the execution of a Professor method.
 
     :version:
     :author:
     """
    pass


class Professor(object):

    """
     Representation of a professor in the data base.

    :version:
    :author:
    """

    """ ATTRIBUTES

     The professor's name.

    name  (public)

     Associated data base key.

    idProfessor  (public)

     Associated database key of the professor's department.

    idDepartment  (public)

     Professor's identification number 0 by default

    memberId  (public)

     Professor's office, can be None
    
    office (public)

     Professor's email, can be None

    email (public)

     Professor's phone number, can be None

    phoneNumber (public)

     Professor's cellphone number, can be None

    cellphoneNumber (public)    
    """

    def __init__(self, name):
        """
         Professor's name is the basic attribute for creating a professor in your data
         base.

        @param string name : The professor's name.
        @return  :
        @author
        """
        if not isinstance(name, (str, unicode)):
            raise ProfessorError('Parameter name must be a string or an unicode')
        self.name = name
        self.idProfessor = None
        self.idDepartment = None
        self.memberId = 0
        self.office = None
        self.email = None
        self.phoneNumber = None
        self.cellphoneNumber = None 

    def __eq__(self, other):
        if not isinstance(other, Professor):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self,other):
        return not self.__eq__(other)

    def setCellphoneNumber(self, cellphoneNumber):
        """
         With the cellphoneNumber parameter given set the cellphoneNumber.

        @param int cellphoneNumber : Professor's cellphone number.
        @return  :
        @author
        """
        if not isinstance(cellphoneNumber, (int, long)):
            raise ProfessorError('Parameter email must be a string or an unicode')
        self.cellphoneNumber = cellphoneNumber

    def setPhoneNumber(self, phoneNumber):
        """
         With the phoneNumber parameter given set the phoneNumber.

        @param int phoneNumber : Professor's phone number.
        @return  :
        @author
        """
        if not isinstance(phoneNumber, (int, long)):
            raise ProfessorError('Parameter email must be a string or an unicode')
        self.phoneNumber = phoneNumber

    def setEmail(self, email):
        """
         With the email parameter given set the email.

        @param string email : Professor's email.
        @return  :
        @author
        """
        if not isinstance(email, (str, unicode)):
            raise ProfessorError('Parameter email must be a string or an unicode')
        self.email = email

    def setOffice(self, office):
        """
         With the office parameter given set the office.

        @param string office : Professor's office.
        @return  :
        @author
        """
        if not isinstance(office, (str, unicode)):
            raise ProfessorError('Parameter office must be a string or an unicode')
        self.office = office

    def setMemberId(self, memberId):
        """
         With the memberId given set the memberId.

        @param memberId int : 
        @return  :
        @author
        """
        if not isinstance(memberId, (int , long)):
            raise ProfessorError('Parameter memberId must be an int or a long')
        self.memberId = memberId
      

    def setDepartment(self, department):
        """
         With the Department objects given set the idDepartment.

        @param Department department : 
        @return  :
        @author
        """
        if not isinstance(department, Department) or not Department.pickById(department.idDepartment) == department :
            raise ProfessorError('Parameter department must be a Department object')
        self.idDepartment = department.idDepartment

    def getDepartment(self):
        """
         Returns the Department object associated with the idDepartment of this object.

        @return Department :
        @author
        """
        
        return Department.pickById(self.idDepartment)


    @staticmethod
    def pickById(idProfessor):
        """
         Returns a single professor with the chosen ID.

        @param int idProfessor : Associated data base key.
        @return Professor :
        @author
        """
        cursor = MySQLConnection()
        try:
            professorData = cursor.execute('SELECT idProfessor, memberId, name, office, email, phoneNumber, cellphoneNumber FROM professor WHERE idProfessor =  '+ str(idProfessor))[0]
        except:
            return None
        professor = Professor(professorData[2])
        professor.idProfessor = professorData[0]
        professor.memberId = professorData[1]
        professor.office = professorData[3]
        professor.email = professorData[4]
        professor.phoneNumber = professorData[5]
        professor.cellphoneNumber = professorData[6]

        #Find the department
        idDepartmentData = cursor.execute('SELECT idDepartment from rel_department_professor WHERE idProfessor = ' + str(idProfessor))
        if len(idDepartmentData) == 1:
            professor.idDepartment = idDepartmentData[0][0]
        return professor

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
         > idProfessor
         > name_equal or name_like
         > memberId
         > department
         > office
         > email
         > phoneNumber
         > cellphoneNumber

         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Professor.find(name_like = "Some Na", department = departmentObject)

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        parameters = {}
        complement = ''
        for key in kwargs:
            if key == 'department':
                complement = ' JOIN rel_department_professor rdp ON rdp.idProfessor = pro.idProfessor'
                parameters['rdp.idDepartment'] = kwargs['department'].idDepartment
            elif key == 'idDepartment':
                complement = ' JOIN rel_department_professor rdp ON rdp.idProfessor = pro.idProfessor'
                parameters['rdp.idDepartment'] = kwargs['idDepartment']
            else:
                parameters['pro.' + key] = kwargs[key]
        professorsData = cursor.find('SELECT pro.name, pro.idProfessor, pro.memberId, pro.office, pro.email, pro.phoneNumber, pro.cellphoneNumber FROM professor pro' + complement ,parameters)
        professors = []
        for professorData in professorsData:
            professor = Professor(professorData[0])
            professor.idProfessor = professorData[1]
            professor.memberId = professorData[2]
            professor.office = professorData[3]
            professor.email = professorData[4]
            professor.phoneNumber = professorData[5]
            professor.cellphoneNumber = professorData[6]
            idDepartmentData = cursor.execute('SELECT idDepartment from rel_department_professor WHERE idProfessor = ' + str(professorData[1]))
            if len(idDepartmentData) == 1:
                professor.idDepartment = idDepartmentData[0][0]
            professors.append(professor)
        return professors

    def store(self):
        """
         Creates or alters the professor's data in the data base.

        @return :
        @author
        """
        cursor = MySQLConnection()
        #First correct the parameters that can be None
        
        if self.office == None:
            mySQLOffice = 'NULL'  #in MySQL is NULL
        else:
            mySQLOffice = '"' + self.office + '"'          

        if self.email == None:
            mySQLEmail = 'NULL'  #in MySQL is NULL
        else:
            mySQLEmail = '"' + self.email + '"'

        if self.phoneNumber == None:
            mySQLPhoneNumber = 'NULL'  #in MySQL is NULL
        else:
            mySQLPhoneNumber = self.phoneNumber

        if self.cellphoneNumber == None:
            mySQLCellphoneNumber = 'NULL'  #in MySQL is NULL
        else:
            mySQLCellphoneNumber = self.cellphoneNumber
   
        if self.idProfessor == None:
            possibleIds = self.find(name_equal = self.name, memberId = self.memberId) #That defines a Professor in the database
            if len(possibleIds) > 0:
                professor = possibleIds[0]
                self.idProfessor = professor.idProfessor
                return
            else:
                query = 'INSERT INTO professor (name, memberId, office, email, phoneNumber, cellphoneNumber) VALUES ("' + self.name + '", ' + str(self.memberId) + ', ' + mySQLOffice + ', ' + mySQLEmail + ', ' + str(mySQLPhoneNumber) + ', ' + str(mySQLCellphoneNumber) + ')'
                cursor.execute(query)
                self.idProfessor = self.find(name_equal = self.name, memberId = self.memberId, office_equal = self.office, email_equal = self.email, phoneNumber = self.phoneNumber, cellphoneNumber = self.cellphoneNumber)[0].idProfessor
        else:
            query = 'UPDATE professor SET name = "' + str(self.name) + '", memberId = ' + str(self.memberId) + ', office = ' + mySQLOffice + ', email = ' + mySQLEmail + ', phoneNumber = ' + str(mySQLPhoneNumber) + ', cellphoneNumber = ' + str(mySQLCellphoneNumber)
            query += " WHERE idProfessor = " +str(self.idProfessor)
            cursor.execute(query)
        #First delete old department relations
        cursor.execute('DELETE FROM rel_department_professor WHERE idProfessor = ' + str(self.idProfessor))
        #Now create the new ones
        if self.idDepartment != None:
            cursor.execute('INSERT INTO rel_department_professor (idProfessor, idDepartment) VALUES (' + str(self.idProfessor) + ', ' + str(self.idDepartment)  + ')')

    def delete(self):
        """
         Deletes the professor's data in the data base.
         
         Return: true if successful or false otherwise

        @return bool :
        @author
        """
        if self.idProfessor != None:
            cursor = MySQLConnection()
            if self == Professor.pickById(self.idProfessor):
                cursor.execute('DELETE FROM rel_department_professor WHERE idProfessor = ' + str(self.idProfessor))
                cursor.execute('DELETE FROM professor WHERE idProfessor = ' + str(self.idProfessor))
            else:
                raise ProfessorError("Can't delete non saved object.")
        else:
            raise ProfessorError('No idProfessor defined.')


