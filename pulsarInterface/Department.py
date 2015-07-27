#encoding: utf8
from tools.MySQLConnection import MySQLConnection

class DepartmentError(Exception):
    """
     Exception reporting an error in the execution of a Department method.

    :version:
    :author:
    """
    pass

class Department(object):

    """
     

    :version:tes
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idDepartment  (public)

     Department name.

    name  (public)

     A string code that represents the department

    departmentCode  (public)

    """
    
    def __init__(self, name, departmentCode):
        """
         Creates a Department object if all the parameters needed are specified.

        @param string name : Department name
        @param string departmentCode : 
        @return  :
        @author
        """
        #Parameters verification.
        if not isinstance(name, (str, unicode)):
            raise DepartmentError('Parameter name must be a string or an unicode.')
        if not isinstance(departmentCode, (str, unicode)):
            raise DepartmentError('Parameter departmentCode must be a string or an unicode.')
        
        #Setting parameters.        
        self.name = name
        self.departmentCode = departmentCode
        #Setting None parameters.        
        self.idDepartment = None
    
    def __eq__(self, other):
        if not isinstance(other, Department):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)


    @staticmethod
    def pickById(idDepartment):
        """
         Searches for a department with the same id as the value of the parameter idDepartment.
         
         Return: one object of the class Department, if successful, or none, if unsuccessful.

        @param int idDepartment : Associated database key.
        @return Department :
        @author
        """
        cursor = MySQLConnection()
        try:
            departmentData = cursor.execute('SELECT * FROM department WHERE idDepartment = ' + str(idDepartment))[0]
        except:
            return None
        department = Department(departmentData[1], departmentData[2])
        department.idDepartment = departmentData[0]
        return department

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
         > idDepartment
         > name_equal or name_like
         > departmentCode_equal or departmentCode_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Department.find(name_equal = "Department of Computer Science",
         departmentCode_like = "MAC")

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        departmentsData = cursor.find('SELECT name, departmentCode, idDepartment FROM department',kwargs)
        departments = []
        for departmentData in departmentsData:
            department = Department(departmentData[0], departmentData[1])
            department.idDepartment = departmentData[2]
            departments.append(department)
        return departments

    def store(self):
        """
         Creates or changes the department's data in the database.
         Return: True if successful or False otherwise.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        if self.idDepartment == None:
            departments = Department.find(name_equal = self.name, departmentCode_equal = self.departmentCode)
            if len(departments) > 0:
                self.idDepartment = departments[0].idDepartment #Any department that fit those parameters is the same as this department, so no need to save
                return
            else:
                #Create this department
                query = 'INSERT INTO department (name, departmentCode) VALUES("' + self.name + '", "' + self.departmentCode + '")'
                cursor.execute(query)
                self.idDepartment = Department.find(name_equal = self.name, departmentCode_equal = self.departmentCode)[0].idDepartment        
        return

    def delete(self):
        """
         Deletes the department's data in the database.
         Return: True if successful or False otherwise.

        @return bool :
        @author
        """
        
        if self.idDepartment != None:
            cursor = MySQLConnection()
            if self == Department.pickById(self.idDepartment):
                cursor.execute('DELETE FROM department WHERE idDepartment = ' + str(self.idDepartment))
                cursor.execute('DELETE FROM rel_department_professor WHERE idDepartment = ' + str(self.idDepartment))
            else:
                raise DepartmentError("Can't delete non saved object.")
        else:
            raise DepartmentError('idDepartment not defined.')



