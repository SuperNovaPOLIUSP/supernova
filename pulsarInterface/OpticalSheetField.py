from pulsarInterface.Offer import Offer
from tools.MySQLConnection import MySQLConnection


class OpticalSheetFieldError(Exception):
    """
     Exception reporting an error in the execution of a OpticalSheetField method.

    :version:
    :author:
    """
    pass


class OpticalSheetField(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idOpticalSheetField  (public)

     Associated database key of the related opticaSheet.

    idOpticalSheet  (public)

     The Offer Object of this relation.

    offer  (public)

     The code of this relation, is None if the opticalSheet is not coded.

    code  (public)

     The position (column) where this offer is in the opticalSheet, more than one
     OpticalSheetField have the same courseIndex, is None if the opticalSheet is
     coded.

    courseIndex  (public)

    """

    def __init__(self, idOpticalSheet, offer):
        """
         Constructor method.

        @param int idOpticalSheet : Associated database key of the related opticaSheet
        @param Offer offer : The Offer Object of this relation.
        @return  :
        @author
        """
        if not isinstance(idOpticalSheet, (int, long)):
            raise OpticalSheetFieldError('Parameter idOpticalSheetField must be an int or long.')

        if not isinstance(offer,Offer) or offer.idOffer == None: #Comparison between offers objects is not made do to efficiency matters.
            raise OpticalSheetFieldError('Parameter offer must be an Offer object that exists in the database.')

        self.offer = offer
        self.idOpticalSheet = idOpticalSheet 
        self.code = None
        self.courseIndex = None 
        self.idOpticalSheetField = None
    
    def __eq__(self, other):
        if not isinstance(other, OpticalSheetField):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)

    def setCode(self, code):
        """
         Set the code of this relation, it should only be used if the OpticalSheet is
         coded.

        @param int code : The code of this relation.
        @return  :
        @author
        """
        if not isinstance(code,(int,long)):
            raise OpticalSheetFieldError('code must be and int or long')
        self.code = code

    def setCourseIndex(self, courseIndex):
        """
         Set the courseIndex of this relation, it should only be used if the OpticalSheet
         is not coded.

        @param int courseIndex : The position (column) where this offer is in the opticalSheet, more than one OpticalSheetField have the same courseIndex.
        @return  :
        @author
        """
        if not isinstance(courseIndex,(int,long)):
            raise OpticalSheetFieldError('courseIndex must be and int or long')
        self.courseIndex = courseIndex

    @staticmethod
    def pickById(idOpticalSheetField):
        """
         Returns one complete OpticalSheetField object where its ID is equal to the
         chosen.

        @param int idOpticalSheetField : Associated database key.
        @return OpticalSheetField :
        @author
        """
        cursor = MySQLConnection()
        opticalSheetFieldData = cursor.execute('SELECT idOpticalSheetField, idOpticalSheet, idOffer, code, courseIndex FROM aggr_opticalSheetField WHERE idOpticalSheetField = ' + str(idOpticalSheetField))[0]
        opticalSheetField = OpticalSheetField(opticalSheetFieldData[1], Offer.pickById(opticalSheetFieldData[2]))
        opticalSheetField.idOpticalSheetField = opticalSheetFieldData[0]
        if opticalSheetFieldData[3] != None:
            opticalSheetField.setCode(opticalSheetFieldData[3])
        elif opticalSheetFieldData[4] != None:
            opticalSheetField.setCourseIndex(opticalSheetFieldData[4])
        return opticalSheetField
    @staticmethod
    def find(**kwargs):
        """
         Searches the database to find one or more objects that fit the description
         specified by the method's parameters. It is possible to perform two kinds of
         search when passing a string as a parameter: a search for the exact string
         (EQUAL operator) and a search for at least part of the string (LIKE operator).
         
         Returns:
         A list of objects that match the specifications made by one (or more) of the
         following parameters:
         > idOpticalSheet
         > idOpticalSheetField
         > offer
         > code
         >courseIndex
         
         E. g. OpticalSheetField.find(idOpticalSheet = 314, offer = Offer, code = 21)

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """

        cursor = MySQLConnection()
        parameters = {}
        for key in kwargs:
            if key == "offer":
                parameters['idOffer'] = kwargs['offer'].idOffer
            else:
                parameters[key] = kwargs[key]
        osfsData = cursor.find('SELECT idOpticalSheetField, idOpticalSheet, idOffer, code, courseIndex FROM aggr_opticalSheetField', parameters)
        osfs = []
        for osfData in osfsData:
            osf = OpticalSheetField(osfData[1], Offer.pickById(osfData[2]))
            osf.idOpticalSheetField = osfData[0]
            if osfData[3] != None:
                osf.setCode(osfData[3])
            elif osfData[4] != None:
                osf.setCourseIndex(osfData[4])
            osfs.append(osf)
        return osfs

    def store(self):
        """
         Stores the information in the database only if either code or courseIndex is not
         None.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        if self.code == None and self.courseIndex == None:
            raise OpticalSheetFieldError("code or courseIndex must be defined")
        if self.code != None and self.courseIndex != None:
            raise OpticalSheetFieldError("code or courseIndex must be undefined")

        if self.code == None:
            mySQLCode = 'NULL'  #in MySQL is NULL
        else:
            mySQLCode = self.code
        if self.courseIndex == None:
            mySQLCourseIndex = 'NULL'
        else:
            mySQLCourseIndex = self.courseIndex
        if self.idOpticalSheetField == None:
            opticalSheetFields = self.find(offer = self.offer, idOpticalSheet = self.idOpticalSheet, code = self.code, courseIndex = self.courseIndex)
            if len(opticalSheetFields) > 0:
                self.idOpticalSheetField = opticalSheetFields[0].idOpticalSheetField #Any osf that fit those parameters is the same as this osf
                return
            else: 
                #Create this osf
                query = 'INSERT INTO aggr_opticalSheetField (idOffer, idOpticalSheet, code, courseIndex) VALUES(' + str(self.offer.idOffer) + ', ' + str(self.idOpticalSheet) + ', ' + str(mySQLCode) + ', ' + str(mySQLCourseIndex) + ')'
                cursor.execute(query)
                self.idOpticalSheetField = self.find(offer = self.offer, idOpticalSheet = self.idOpticalSheet, code = self.code, courseIndex = self.courseIndex)[0].idOpticalSheetField
        else:
            #Update opticalSheetField
            query = 'UPDATE aggr_opticalSheetField SET idOffer = ' + str(self.offer.idOffer) + ', idOpticalSheet = ' + str(self.idOpticalSheet) + ', code = ' + str(mySQLCode) + ', courseIndex = ' + str(mySQLCourseIndex) + ' WHERE idOpticalSheetField = ' + str(self.idOpticalSheetField)
            cursor.execute(query)


    def delete(self):
        """
         Deletes the information in the database.

        @return  :
        @author
        """
        if self.idOpticalSheetField != None:
            cursor = MySQLConnection()
            if self == OpticalSheetField.pickById(self.idOpticalSheetField):
                cursor.execute('DELETE FROM aggr_opticalSheetField WHERE idOpticalSheetField = ' + str(self.idOpticalSheetField))
            else:
                raise OpticalSheetFieldError("Can't delete non saved object.")
        else:
            raise OpticalSheetFieldError('No idOpticalSheetField defined.')



