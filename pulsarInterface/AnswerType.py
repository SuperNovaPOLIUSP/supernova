#coding: utf8

from tools.MySQLConnection import MySQLConnection

class AnswerTypeError(Exception):
    """
     Exception that reports errors during the execution of AnswerType class methods
  
    :version:
    :author:
    """
    pass

class AnswerType(object):

    """
     Class that represents a category of multiple choice answers that a question can
     be related to (e. g. the answer type "hours" may refer to different ammounts of
     hours specified by alternatives A to E).

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idAnswerType  (private)

     A dictionary containing the meaning of the answers alternative choices in the
     form { 'A':'meaningA' , 'B':'meaningB' , ..., 'E':'meaningE'}

    alternativeMeaning  (private)

     The name of the AnswerType related to a category of answers (e.g. hours, frequency).

    name  (private)

    """

    def __init__(self, name, alternativeMeaning):
        """
         Constructor method.
         Name and meaning are the necessary data to create an AnswerType.

        @param string name : The name of the AnswerType related to a category of answers (e.g. hours, frequency).
        @param string{} alternativeMeaning : A dictionary containing the meaning of the answers alternative choices in the form { 'A':'meaningA' , 'B':'meaningB' , ..., 'E':'meaningE'}
        @return  :
        @author
        """
        self.setName(name)
        self.setAlternativeMeaning(alternativeMeaning)

    def __eq__(self, other):
        """
         Comparison method that returns True if two objects of the class AnswerType are
         equal.

        @param AnswerType other : Other object of the class AnswerType to be compared with a present object.
        @return bool :
        @author
        """
        if not isinstance(other, AnswerType):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
         Comparison method that returns True if two objects of the class AnswerType are
         not equal.

        @param AnswerType other : Other object of the class AnswerType to be compared with a present object.
        @return bool :
        @author
        """
        return not self.__eq__(other)

    def setName(self, name):
        """
         Changes the name of the category related to the answer type.

        @param string name : The name of the AnswerType related to a category of answers (e.g. hours, frequency).
        @return  :
        @author
        """
        # verifies if name is a proper parameter
        if isinstance(name, (unicode, str)):
            self.name = name
        else:
            raise AnswerTypeError("Invalid name parameter. It must be of type str or unicode.")

    def setAlternativeMeaning(self, alternativeMeaning):
        """
         Changes the set of alternative meanings of the answer type.

        @param string{} alternativeMeaning : A dictionary containing the meaning of the answers alternative choices in the form { 'A':'meaningA' , 'B':'meaningB' , ..., 'E':'meaningE'}
        @return  :
        @author
        """
        # verifies if alternativeMeaning is a proper parameter
        if isinstance(alternativeMeaning, dict):
            if len(alternativeMeaning) is 5:
                alternativeLetters = alternativeMeaning.keys()
                if ('A' in alternativeLetters) and ('B' in alternativeLetters) and ('C' in alternativeLetters) and ('D' in alternativeLetters) and ('E' in alternativeLetters):
                    for meaning in alternativeMeaning.values():
                        if not isinstance(meaning, (unicode, str)):
                            raise AnswerTypeError("Invalid meaning found.")
                    self.alternativeMeaning = alternativeMeaning
                else:
                    raise AnswerTypeError("Invalid set of alternatives. The parameter alternativeMeaning must be a dictionary with five keys, each key being a leter from A to E.")
            else:
                raise AnswerTypeError("Invalid set of alternatives. The parameter alternativeMeaning must be a dictionary with five keys, each key being a leter from A to E.")
        else:                    
            raise AnswerTypeError("Invalid set of alternatives. The parameter alternativeMeaning must be a dictionary with five keys, each key being a leter from A to E.")

    @staticmethod
    def pickById(idAnswerType):
        """
         Returns an AnswerType object given an idAnswerType.

        @param int idAnswerType : Associated database key.
        @return AnswerType :
        @author
        """
        # gets connection with the mysql database
        databaseConnection = MySQLConnection() 

        # finds the name of the answer type through the answerType table
        name = databaseConnection.execute("SELECT name FROM answerType WHERE idAnswerType = " + str(idAnswerType))

        # tests if the name found is valid
        if len(name) > 0:
            name = name[0][0]
        else:
            return None

        # finds the meaning of each alternative associated to the answer type through the alternativeMeaning table
        alternativeMeaning = databaseConnection.execute("SELECT alternative, meaning FROM alternativeMeaning WHERE idAnswerType = " + str(idAnswerType))
        # turns de result found into a dictionary
        alternativeMeaning = {alternative : meaning for (alternative, meaning) in alternativeMeaning}

        # creates the AnswerType object to be returned
        pickedAnswerType = AnswerType(name, alternativeMeaning)
        pickedAnswerType.idAnswerType = idAnswerType

        return pickedAnswerType

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
         folowing parameters:
         > idAnswerType
         > name_equal or name_like
         > alternativeMeaning_equal or alternativeMeaning_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.

         In this method: the parameter alternativeMeaning_like refers to a dictionary of 
         strings (including empty strings, if needed) that must be all present in the 
         alternatives of the object that needs to be found; and the parameter 
         alternativeMeaning_equal refers to a dictionary containing the exact 
         alternatives of the object that needs to be found.

         E. g. AnswerType.find(name_equal = "time", meaning_like = ["very", "interesting", "good", "less", "bad", "issue"])

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        # gets connection with the mysql database
        databaseConnection = MySQLConnection()

        # finds the database IDs of the answer types that need to be found
        foundAnswerTypeIdsByMeaning = []
        foundAnswerTypeIds = []
        emptyFind = False

        # verifies if the search has been made without any arguments
        # in this case, the method must return all of the AnswerType objects in the database
        if len(kwargs) == 0:
            emptyFind = True

        if "alternativeMeaning_like" in kwargs:
            query = "SELECT idAnswerType FROM alternativeMeaning WHERE"
            for alternative, meaning in kwargs['alternativeMeaning_like'].items():
                query += "(meaning LIKE '%" + meaning + "%' AND alternative = '" + alternative + "') OR "
            query = query[:-4] # removes last ' OR ' inserted
            query += "GROUP BY idAnswerType HAVING count(idAnswerType) = 5"
            foundAnswerTypeIdsByMeaning = databaseConnection.execute(query)

            # changes the result found to a list, instead of a tuple of tuples
            foundAnswerTypeIdsByMeaning = [int(foundAnswerTypeId[0]) for foundAnswerTypeId in foundAnswerTypeIdsByMeaning]

            # removes the 'meaning_like' key from kwargs in order to call the MySQLConnection find method
            del kwargs['alternativeMeaning_like']

        elif "alternativeMeaning_equal" in kwargs:
            # finds the IDS of the database objects that contains the dictionary of meanings passed
            query = "SELECT idAnswerType FROM alternativeMeaning WHERE"
            for alternative, meaning in kwargs['alternativeMeaning_equal'].items():
                query += "(meaning = '" + meaning + "' AND alternative = '" + alternative + "') OR "
            query = query[:-4] # removes last ' OR ' inserted
            query += "GROUP BY idAnswerType HAVING count(idAnswerType) = 5"
            foundAnswerTypeIdsByMeaning = databaseConnection.execute(query)
            foundAnswerTypeIdsByMeaning = [int(foundAnswerTypeId[0]) for foundAnswerTypeId in foundAnswerTypeIdsByMeaning]

            # removes the 'meaning_equal' key from kwargs in order to call the MySQLConnection find method
            del kwargs['alternativeMeaning_equal']

        # gets the intersection of the previously found IDs with those which will be found when searching for the names of the answer types, but only if necessary
        if len(foundAnswerTypeIdsByMeaning) > 0:
            # finds the IDs of the database objects that contain the name or the idAnswerType specified in kwargs
            foundAnswerTypeIds = databaseConnection.find("SELECT idAnswerType FROM answerType", kwargs)
            foundAnswerTypeIds = [int(foundAnswerTypeId[0]) for foundAnswerTypeId in foundAnswerTypeIds]

            # gets the intersection between the two sets of IDs that were found
            foundAnswerTypeIds = list(set(foundAnswerTypeIds).intersection(foundAnswerTypeIdsByMeaning))

        elif len(kwargs) > 0 or emptyFind:
            foundAnswerTypeIds = databaseConnection.find("SELECT idAnswerType FROM answerType", kwargs)
            foundAnswerTypeIds = [int(foundAnswerTypeId[0]) for foundAnswerTypeId in foundAnswerTypeIds]

        # for each ID found, creates an AnswerType object using the 'pickById' method
        foundAnswerTypes = []
        for Id in foundAnswerTypeIds:
            foundAnswerTypes.append(AnswerType.pickById(Id))

        return foundAnswerTypes

    def store(self):
        """
         Changes object on table or adds it to database if an object is absent.

        @return  :
        @author
        """
        # gets connection with the mysql database
        databaseConnection = MySQLConnection()
       
        # does several queries in order to determine, later, the conditions that must be satisfied in order to store the object
        sameMeaningAnswerTypes = AnswerType.find(alternativeMeaning_equal = self.alternativeMeaning)
        sameNameAnswerTypes = AnswerType.find(name_equal = self.name)
        sameNameAndMeaningAnswerTypes = AnswerType.find(alternativeMeaning_equal = self.alternativeMeaning, name_equal = self.name)

        # verifies if the database already has an object like the one to be stored
            
        # if the alternatives exist and the name doesn't, the name in the database must be replaced by the object's name
        if len(sameMeaningAnswerTypes) == 1 and len(sameNameAnswerTypes) == 0:
            databaseConnection.execute("UPDATE answerType SET name = '" + self.name + "' WHERE idAnswerType = " + str(sameMeaningAnswerTypes[0].idAnswerType))

            # assigns the objects associated ID
            self.idAnswerType = sameMeaningAnswerTypes[0].idAnswerType

        # if the name exists and the alternatives don't, the alternatives in the database must be replaced by the object's alternatives
        elif len(sameMeaningAnswerTypes) == 0 and len(sameNameAnswerTypes) == 1:
            for alternative, meaning in self.alternativeMeaning.items():
                databaseConnection.execute("UPDATE alternativeMeaning SET meaning = '" + meaning + "' WHERE alternative = '" + alternative + "' AND idAnswerType = " + str(sameNameAnswerTypes[0].idAnswerType))

            # assigns the objects associated ID
            self.idAnswerType = sameNameAnswerTypes[0].idAnswerType

        # if both the name and the alternatives exist, the object exists in the database
        # if the object still doesn't have its associated ID, this ID is retrieved and assigned to its respective attribute
        elif len(sameNameAndMeaningAnswerTypes) == 1:
            if not hasattr(self, 'idAnswerType'):
                self.idAnswerType = sameNameAndMeaningAnswerTypes[0].idAnswerType

        # if both the alternative and the name doesn't exist, the object is new and must be created
        elif len(sameNameAnswerTypes) == 0 and len(sameMeaningAnswerTypes) == 0 and len(sameNameAndMeaningAnswerTypes) == 0:
            databaseConnection.execute("INSERT INTO answerType (name) VALUES ('" + self.name + "')")
            # retrieves the idAnswerType for the most recently created object
            self.idAnswerType = int(databaseConnection.execute("SELECT idAnswerType FROM answerType WHERE name = '" + self.name + "'")[0][0])
            # inserts alternative meanings in the database
            for alternative, meaning in self.alternativeMeaning.items():
                databaseConnection.execute("INSERT INTO alternativeMeaning (idAnswerType, alternative, meaning) VALUES (" + str(self.idAnswerType) + ", '" + alternative + "', '" + meaning + "')")

        else:
            pass

        
    def delete(self):
        """
         Deletes object from the database.

        @return  :
        @author
        """
        
        if not hasattr(self, 'idAnswerType'):
            pass 
        else:
            # gets connection with the mysql database
            databaseConnection = MySQLConnection()

            # deletes from the alternativeMeaning table
            databaseConnection.execute("DELETE FROM alternativeMeaning WHERE idAnswerType = " + str(self.idAnswerType))
            # deletes from the answerType table
            databaseConnection.execute("DELETE FROM answerType WHERE idAnswerType = " + str(self.idAnswerType))
       
