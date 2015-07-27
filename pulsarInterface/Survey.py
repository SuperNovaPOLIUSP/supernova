from pulsarInterface.Questionnaire import Questionnaire
from tools.MySQLConnection import MySQLConnection


class SurveyError(Exception):
    """
     Exception reporting an error in the execution of a Offer method.

    :version:
    :author:
    """
    pass

class Survey(object):

    """
     Class representing a survey. Each object may be related to one of several
     assessments made during a time period (e.g. first assessment, second assessment,
     etc.).

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idSurvey  (public)

     Associated database key of the related opticaSheet.

    idOpticalSheet  (public)

     Related questionnaire.

    questionnaire  (public)

     if it is the first, the second, etc. assessment process made in this time
     period.

    assessmentNumber  (public)

    """

    def __init__(self, idOpticalSheet, questionnaire, assessmentNumber):
        """
         Constructor method.

        @param int idOpticalSheet : Associated database key of the related opticaSheet.
        @param Questionnaire questionnaire : Related questionnaire.
        @param int assessmentNumber : if it is the first, the second, etc. assessment process made in this time period.
        @return  :
        @author
        """
        if not isinstance(idOpticalSheet, (int, long)):
            raise SurveyError('Parameter idOpticalSheet must be an int or long.')
        if not isinstance(assessmentNumber, (int, long)):
            raise SurveyError('Parameter assessmentNumber must be an int or long.')
        if not isinstance(questionnaire, Questionnaire) or not Questionnaire.pickById(questionnaire.idQuestionnaire) == questionnaire:
            raise SurveyError('Parameter questionnaire must be a Questionnaire object that exists in the database.')

        self.questionnaire = questionnaire
        self.idOpticalSheet = idOpticalSheet
        self.assessmentNumber = assessmentNumber 
        self.idSurvey = None

    def __eq__(self, other):
        if not isinstance(other, Survey):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)


    @staticmethod
    def pickById(idSurvey):
        """
         Returns one complete Survey object where its ID is equal to the chosen.

        @param int idSurvey : Associated database key.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        surveyData = cursor.execute('SELECT idOpticalSheet, idQuestionnaire, assessmentNumber FROM aggr_survey WHERE idSurvey = ' + str(idSurvey))[0]
        survey = Survey(surveyData[0], Questionnaire.pickById(surveyData[1]), surveyData[2])
        survey.idSurvey = idSurvey
        return survey

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
         > idSurvey
         > questionnaire
         > assessmentNumber
         
         E. g. Survey.find(idOpticalSheet = 314, questionnaire = Questionnaire,
         assessmentNumber = 1)

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        parameters = {}
        for key in kwargs:
            if key == "questionnaire":
                parameters['idQuestionnaire'] = kwargs['questionnaire'].idQuestionnaire
            else:
                parameters[key] = kwargs[key]
        surveysData = cursor.find('SELECT idSurvey, idOpticalSheet, idQuestionnaire, assessmentNumber FROM aggr_survey', parameters)
        surveys = []
        for surveyData in surveysData:
            survey = Survey(surveyData[1], Questionnaire.pickById(surveyData[2]), surveyData[3])
            survey.idSurvey = surveyData[0]
            surveys.append(survey)
        return surveys

    def store(self):
        """
         Stores the information in the database.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        if self.idSurvey == None:
            #Try to find this survey in the database
            surveys = self.find(idOpticalSheet = self.idOpticalSheet, questionnaire = self.questionnaire, assessmentNumber = self.assessmentNumber)
            if len(surveys) > 0:
                #The survey already exist in the database, no need to do nothing
                self.idSurvey = surveys[0].idSurvey #Any survey that fit those parameters is the same as this survey
                return
            else:
                #Create this survey
                cursor.execute('INSERT INTO aggr_survey (idOpticalSheet, idQuestionnaire, assessmentNumber) VALUES(' + str(self.idOpticalSheet) + ', ' + str(self.questionnaire.idQuestionnaire) + ', ' + str(self.assessmentNumber) + ')')
                self.idSurvey = self.find(idOpticalSheet = self.idOpticalSheet, questionnaire = self.questionnaire, assessmentNumber = self.assessmentNumber)[0].idSurvey
        #in this class there is no update, so if idSurvey != None no need to do nothing

    def delete(self):
        """
         Deletes the information in the database.

        @return  :
        @author
        """
        if self.idSurvey != None:
            cursor = MySQLConnection()
            if self == Survey.pickById(self.idSurvey):
                cursor.execute('DELETE FROM aggr_survey WHERE idSurvey = ' + str(self.idSurvey))
            else:
                raise SurveyError("Can't delete non saved object.")
        else:
            raise SurveyError('No idSurvey defined.')


