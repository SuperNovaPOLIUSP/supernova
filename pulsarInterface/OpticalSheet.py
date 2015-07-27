#coding: utf8
from pulsarInterface.Cycle import Cycle
from pulsarInterface.Offer import Offer
from pulsarInterface.OpticalSheetField import OpticalSheetField
from pulsarInterface.Questionnaire import Questionnaire
from pulsarInterface.Survey import Survey
from tools.MySQLConnection import MySQLConnection


class OpticalSheetError(Exception):
    """
     Exception reporting an error in the execution of a OpticalSheetColumn method.

    :version:
    :author:
    """
    pass



class OpticalSheet (object):

    """
     Contains the information of an Optical Sheet from the Data Base. It also makes
     and saves alterations.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idOpticalSheet  (public)

    A string specifying the type of survey that will be used as is defined by minitableSurveyType.

    surveyType  (public)

    Id related to surveyType, as defined in the minitableSurveyType.

    idSurveyType  (public)

     List of dictionaries in the form [{"term" : termOfTheCycle, "cycle" :
     cycleObject },{...].

    cycles  (public)

     List of surveys associated to this Optical Sheet.

    surveys  (public)

     A list of OpticalSheetField objects.

    fields  (public)

     The name of the encoding in the opticalSheet, it defines the opticalSheet as encoded
    
    encodingName (public)

    """

    def __init__(self, surveyType):
        """
         

        @param string surveyType : A string specifying the type of survey that will be used as is defined by minitableSurveyType.
        @return  :
        @author
        """
        if not isinstance(surveyType, (str, unicode)):
            raise OpticalSheetError('Parameter surveyType must be a string')
        else:
            cursor = MySQLConnection()
            try:
                idSurveyType = cursor.execute('SELECT idSurveyType FROM minitableSurveyType WHERE typeName = "' + surveyType + '"')[0][0]
            except:
                raise OpticalSheetError('Parameter surveyType must be a defined in the minitableSurveyType')
        self.idSurveyType = idSurveyType
        self.surveyType = surveyType
        self.idOpticalSheet = None
        self.cycles = []
        self.surveys = []
        self.fields = None
        self.encodingName = None

    def __eq__(self, other):
        if not isinstance(other, OpticalSheet):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)

    

    def setEncodingName(self, encodingName):
        """
         Set the opticalSheet's encoding name, this defines the opticalSheet as encoded.
        @param str encodingName : OpticalSheet's encoding name
        @return :
        @author
        """
        if not isinstance(encodingName, (str, unicode)):
            raise OpticalSheetError('EncodingName must be string or unicode.')
        self.encodingName = encodingName

    def addSurvey(self, questionnaire, assessmentNumber):
        """
         Creates and adds a survey to the surveys list with the parameters passed. In
         case there is already a survey belonging to the same assessment, or if it is not
         possible to add the survey for any other reason, returns False.

        @param undef questionnaire : Questionnaire to be associated to this Optical Sheet.
        @param undef assessmentNumber : if it is the first, the second, etc. assessment process made in this time period.
        @return  :
        @author
        """
        if self.idOpticalSheet == None:
            raise OpticalSheetError('idOpticalSheet parameter must be defined in order to add surveys')
        if not isinstance(questionnaire, Questionnaire) or not Questionnaire.pickById(questionnaire.idQuestionnaire) == questionnaire:
            raise OpticalSheetError('Parameter questionnaire must be a Questionnaire objects that exists in the database.')
        for survey in self.surveys:
            if survey.assessmentNumber == assessmentNumber:
                raise OpticalSheetError("There can't be more than one survey with the same assessment number in one opticalSheet.")
        self.surveys.append(Survey(self.idOpticalSheet, questionnaire, assessmentNumber))
        

    def removeSurvey(self, assessmentNumber):
        """
         Removes the survey from the list (surveys) with this assessmentNumber and
         returns False if it does not work.

        @param undef assessmentNumber : if it is the first, the second, etc. assessment process made in this time period.
        @return undef :
        @author
        """
        if not isinstance(assessmentNumber,(int, long)):
            raise OpticalSheetError("Parameter assessmentNumber must be int or long")
        self.surveys = [survey for survey in self.surveys if survey.assessmentNumber != assessmentNumber]

    def addOpticalSheetField(self, offers, index):
        """
         Adds an OpticalSheetField relating the set of offers to thisopticalSheet, if this opticalSheet encodingName is None the offer is added in courseIndex, if the encodingName is defined, the offer is added in code

        @param Offer[] offers : List of offers to be appended to this Optical Sheet.
        @param int index : Index/code of the offers to be appended.
        @return  :
        @author
        """
        if self.idOpticalSheet == None:
            raise OpticalSheetError('idOpticalSheet parameter must be defined in order to add offers')
        if self.fields == None:
            self.fields = []
        for offer in offers:
            #Check if is a valid Offer object
            if not isinstance(offer,Offer):
                raise OpticalSheetError('Parameter offers must be a list of Offer object.')
            if not Offer.pickById(offer.idOffer) == offer:
                raise OpticalSheetError('Parameter offers must exists in the database.')
            #Create an OpticalSheetColumn for this offer and this index
            opticalSheetField = OpticalSheetField(self.idOpticalSheet, offer)
            if self.encodingName != None:
                opticalSheetField.setCode(index)
            else:
                opticalSheetField.setCourseIndex(index)
            self.fields.append(opticalSheetField)


    def removeOpticalSheetField(self, index):
        """
         Removes an OpticalSheetField with the selected index in this opticalSheet.

        @param int index : Index/code of the offers to be removed.
        @return  :
        @author
        """
        if not isinstance(index,(int, long)):
            raise OpticalSheetError("Parameter index must be int or long")
        self.fields = [field for field in self.fields if field.code != index and field.courseIndex != index]

    def addCycle_Term(self, cycle, term):
        """
         Adds a cycle's term to the Optical  Sheet.

        @param Curriculo cycle : Cycle to be associated to this Optical Sheet
        @param int term : Term of the cycle to be appended to this Optical Sheet.
        @return  :
        @author
        """
        if not isinstance(cycle,Cycle) or not cycle == Cycle.pickById(cycle.idCycle):
            raise OpticalSheetError('Parameter cycle must be a Cycle object that exists in the database.')
        if not isinstance(term,(int,long)):
            raise OpticalSheetError('Parameter term must be a long or an int')
        self.cycles.append({'cycle':cycle, 'term':term})

    def removeCycle_Term(self, cycle, term):
        """
         Removes a cycle's term from this Optical Sheet.

        @param Curriculo cycle : Cycle to be associated to this Optical Sheet
        @param int term : Term of the cycle to be appended to this Optical Sheet.
        @return  :
        @author
        """
        if not isinstance(cycle,Cycle) or not cycle == Cycle.pickById(cycle.idCycle):
            raise OpticalSheetError('Parameter cycle must be a Cycle object that exists in the database.')
        if not isinstance(term,(int,long)):
            raise OpticalSheetError('Parameter term must be a long or an int')
        self.cycles.remove({'cycle':cycle,'term':term}) 


    def fillCycles(self):
        cursor = MySQLConnection()
        self.cycles = []
        cyclesData = cursor.execute('SELECT idCycle, term FROM rel_cycle_opticalSheet WHERE idOPticalSheet = ' + str(self.idOpticalSheet))
        for cycleData in cyclesData:
            self.cycles.append({'cycle':Cycle.pickById(cycleData[0]), 'term':cycleData[1]})

    def fillOpticalSheetFields(self):
        self.fields = OpticalSheetField.find(idOpticalSheet = self.idOpticalSheet)

    def fillSurveys(self):
        cursor = MySQLConnection()
        self.surveys = []
        surveysData = cursor.execute('SELECT idSurvey FROM aggr_survey WHERE aggr_survey.idOpticalSheet = ' + str(self.idOpticalSheet))
        assessmentNumbers = []
        for surveyData in surveysData:
            survey = Survey.pickById(surveyData[0])
            if survey.assessmentNumber in assessmentNumbers:
                raise OpticalSheetError("There can't be more than one survey with the same assessment number in one opticalSheet.")
            assessmentNumbers.append(survey.assessmentNumber)
            self.surveys.append(survey)

    @staticmethod
    def pickById(idOpticalSheet):
        """
         Returns one complete Optical Sheet object where its ID is equal to the chosen.

        @param int idOpticalSheet : Associated data base key.
        @return OpticalSheet :
        @author
        """
        cursor = MySQLConnection()
        opticalSheetData = cursor.execute('SELECT minitableSurveyType.typeName FROM opticalSheet JOIN minitableSurveyType ON minitableSurveyType.idSurveyType = opticalSheet.idSurveyType WHERE opticalSheet.idOpticalSheet = ' + str(idOpticalSheet))
        if len(opticalSheetData) == 0:
            return None
        else:
            opticalSheetData = opticalSheetData[0]
        opticalSheet = OpticalSheet(opticalSheetData[0])
        opticalSheet.idOpticalSheet = idOpticalSheet
        opticalSheet.fillSurveys()
        opticalSheet.fillCycles()
        #opticalSheet.fillOpticalSheetFields() #it takes a long to do it
        encodedData = cursor.execute('SELECT name FROM encoding WHERE idOpticalSheet = ' + str(idOpticalSheet))
        if len(encodedData) > 0:
            opticalSheet.setEncodingName(encodedData[0][0])
        return opticalSheet
        

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
         > idOpticalSheet
         > surveyType
         > cycles
         > term
         > questionnaires
         > offers
         > timePeriod
         > encodingName
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. OpticalSheet.find(surveyType_like = "n", cycles = listOfCycleObjects, timePeriod = TimePeriodObject)

        @param undef _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        parameters = {}
        complement = ''
        for key in kwargs:
            if key == 'surveyType_equal':
                parameters['minitableSurveyType.typeName_equal'] = kwargs[key]
            elif key == 'surveyType_like':
                parameters['minitableSurveyType.typeName_like'] = kwargs[key]
            elif key == 'term':
                if not 'cycles' in kwargs.keys():
                    complement = complement + ' JOIN rel_cycle_opticalSheet ON rel_cycle_opticalSheet.idOpticalSheet = opticalSheet.idOpticalSheet'
                parameters['rel_cycle_opticalSheet.term'] = kwargs[key]
            elif key == 'cycles':
                complement = complement + ' JOIN rel_cycle_opticalSheet ON rel_cycle_opticalSheet.idOpticalSheet = opticalSheet.idOpticalSheet'
                parameters['rel_cycle_opticalSheet.idCycle'] = [cycle.idCycle for cycle in kwargs[key]]
            elif key == 'questionnaires':
                complement = complement + ' JOIN aggr_survey ON aggr_survey.idOpticalSheet = opticalSheet.idOpticalSheet'
                parameters['aggr_survey.idQuestionnaire'] = [questionnaire.idQuestionnaire for questionnaire in kwargs[key]]
            elif key == 'offers':
                complement = complement + ' JOIN aggr_opticalSheetField ON aggr_opticalSheetField.idOpticalSheet = opticalSheet.idOpticalSheet'
                parameters['aggr_opticalSheetField.idOffer'] = [offer.idOffer for offer in kwargs[key]]
            elif key == 'timePeriod':
                if not 'offers' in kwargs.keys():
                    complement = complement + ' JOIN aggr_opticalSheetField ON aggr_opticalSheetField.idOpticalSheet = opticalSheet.idOpticalSheet JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer'
                else:
                    complement = complement + ' JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer'
                parameters['aggr_offer.idTimePeriod'] = kwargs[key].idTimePeriod
            elif key == 'encodingName_like' or key == 'encodingName_equal':
                complement = complement + ' JOIN encoding ON encoding.idOpticalSheet = opticalSheet.idOpticalSheet'
                parameters['encoding.name_' + key.split('_')[1]] = kwargs[key] 
            else:
                parameters['opticalSheet.' + key] = kwargs[key]
        opticalSheetsData = cursor.find('SELECT opticalSheet.idOpticalSheet, minitableSurveyType.typeName FROM opticalSheet JOIN minitableSurveyType ON minitableSurveyType.idSurveyType = opticalSheet.idSurveyType' + complement, parameters, ' GROUP BY opticalSheet.idOpticalSheet')
        opticalSheets = []
        for opticalSheetData in opticalSheetsData:
            opticalSheet = OpticalSheet(opticalSheetData[1])
            opticalSheet.idOpticalSheet = opticalSheetData[0]
            opticalSheet.fillSurveys()
            opticalSheet.fillCycles()
            encodedData = cursor.execute('SELECT name FROM encoding WHERE idOpticalSheet = ' + str(opticalSheet.idOpticalSheet))
            if len(encodedData) > 0:
                opticalSheet.setEncodingName(encodedData[0][0])
            opticalSheets.append(opticalSheet)
        return opticalSheets

    def storeDatafile(self, datafile, assessmentNumber):
        """
         Store a Datafile object along with its answers, and return the answers that
         couldn't be stored.
 
        @param answer.Datafile datafile : Datafile to be stored (including its answers) to this opticalSheet.
        @return answer.Answer[] :
        @author
        """
        cursor = MySQLConnection()
        if self.idOpticalSheet == None:
            OpticalSheetError("You can't save a datafile in an non saved OpticalSheet")
        thisSurvey = None
        for survey in self.surveys:
            if survey.assessmentNumber == assessmentNumber:
                thisSurvey = survey
                break
        if thisSurvey == None:
            OpticalSheetError("This chosen assessmentNumber doesn't exist")
        if self.fields == None:
            self.fillOpticalSheetFields()
            if self.fields == None:
                OpticalSheetError("This opticalSheet doesn't have fields")
        #First find the last used id
        lastId = cursor.execute('SELECT idAnswer FROM answer ORDER BY idAnswer DESC LIMIT 1;')[0][0]
        query1 = 'INSERT INTO answer(idAnswer, questionIndex, idDatafile, alternative, identifier) VALUES'
        query2 = 'INSERT INTO rel_answer_opticalSheetField_survey(idAnswer, idOpticalSheetField, idSurvey) VALUES '
        query1Check = False
        query2Check = False
        datafile.store()
        errors = []
        for answer in datafile.answers:
            lastId = lastId + 1
            query1Check = True
            query1 = query1 + '(' + str(lastId) + ' ,' + str(answer.questionIndex) + ', ' + str(datafile.idDatafile) + ', "' + answer.alternative + '", ' + str(answer.identifier) + '), '
            chosenFields = []
            print 'len(fields)=', len(self.fields)
            print answer.__dict__
            for field in self.fields:
                if self.encodingName == None: #OpticalSheet is not encoded
                    if field.courseIndex == answer.courseIndex and field.offer.classNumber == answer.code:
                        chosenFields.append(field)
                else:
                    if field.code == answer.code:
                        chosenFields.append(field)
            print 'len(chosenFields)=', len(chosenFields)
            if len(chosenFields) == 0:
                errors.append(answer)
            for chosenField in chosenFields:
                query2Check = True
                query2  = query2 + '(' + str(lastId) + ', ' + str(chosenField.idOpticalSheetField) + ' ,' + str(thisSurvey.idSurvey) + '), '
        query2 = query2[:-2]
        query1 = query1[:-2]
        print query2Check, query2
        if query1Check:
            cursor.execute(query1)
        if query2Check:
            cursor.execute(query2)
        return errors
           

    def store(self):
        """
         Saves the information in the database.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        if self.idOpticalSheet == None:
            cursor.execute('INSERT INTO opticalSheet (idSurveyType) VALUES (' + str(self.idSurveyType) + ')') 
            self.idOpticalSheet = cursor.execute('SELECT LAST_INSERT_ID()')[0][0]
        if len(cursor.execute('SELECT * FROM rel_answer_opticalSheetField_survey JOIN aggr_opticalSheetField ON aggr_opticalSheetField.idOpticalSheetField = rel_answer_opticalSheetField_survey.idOpticalSheetField WHERE aggr_opticalSheetField.idOpticalSheet = ' + str(self.idOpticalSheet))) == 0:
            #NOW Update cycles relation
            cursor.execute('DELETE FROM rel_cycle_opticalSheet WHERE idOpticalSheet = ' + str(self.idOpticalSheet)) #Delete all the old ones
            for cycle in self.cycles:
                cursor.execute('INSERT INTO rel_cycle_opticalSheet (idOpticalSheet, idCycle, term) VALUES (' + str(self.idOpticalSheet) + ', ' + str(cycle['cycle'].idCycle) + ', ' + str(cycle['term']) + ')')
            if self.encodingName != None:
                cursor.execute('DELETE FROM encoding WHERE idOpticalSheet = ' + str(self.idOpticalSheet))
                cursor.execute('INSERT INTO encoding (idOpticalSheet, name) VALUES (' + str(self.idOpticalSheet) + ', "' + self.encodingName + '")')
            #NOW Update the fields
            if self.fields != None:
                newFields = self.fields
                self.fillOpticalSheetFields() #First find the old fields
                if self.fields != newFields:
                    fieldsToRemove = [oldField for oldField in self.fields if oldField not in newFields] #Find the fields that don't belong to the new list
                    fieldsToAdd = [newField for newField in newFields if newField not in self.fields] #Find the fields that don't belong to the old list
                    for field in fieldsToRemove:
                        field.delete()
                    for field in fieldsToAdd:
                        field.store()
                self.fields = newFields

        newSurveys = self.surveys
        self.fillSurveys() #to find the old surveys
        oldSurveys = self.surveys
        #now compare them
        if oldSurveys != newSurveys:
            surveysToRemove = [oldSurvey for oldSurvey in oldSurveys if oldSurvey not in newSurveys]
            surveysToAdd = [newSurvey for newSurvey in newSurveys if newSurvey not in oldSurveys]
            finalSurveys = []
            for survey in surveysToRemove:
                if len(cursor.execute('SELECT * FROM rel_answer_opticalSheetField_survey JOIN aggr_survey ON aggr_survey.idSurvey = rel_answer_opticalSheetField_survey.idSurvey WHERE aggr_survey.idOpticalSheet = ' + str(self.idOpticalSheet) + ' AND aggr_survey.assessmentNumber = ' + str(survey.assessmentNumber))) == 0:
                    survey.delete()
                else:
                    finalSurveys.append(survey) #If they have answers they won't be deleted
            for survey in surveysToAdd:
                if len(cursor.execute('SELECT * FROM rel_answer_opticalSheetField_survey JOIN aggr_survey ON aggr_survey.idSurvey = rel_answer_opticalSheetField_survey.idSurvey WHERE aggr_survey.idOpticalSheet = ' + str(self.idOpticalSheet) + ' AND aggr_survey.assessmentNumber = ' + str(survey.assessmentNumber))) == 0:
                    survey.store()
                    finalSurveys.append(survey) #If there are no answers put the new one
        #now put the real ones in the opticalSheet
            self.surveys = finalSurveys


    def delete(self):
        """
         Deletes the information in the database.

        @return  :
        @author
        """
        if self.idOpticalSheet != None:
            cursor = MySQLConnection()
            tempOpticalSheet = OpticalSheet.pickById(self.idOpticalSheet)
            if self.fields != None:
                tempOpticalSheet.fillOpticalSheetFields()
            if self == tempOpticalSheet:
                cursor.execute('DELETE FROM rel_cycle_opticalSheet WHERE idOpticalSheet = ' + str(self.idOpticalSheet))
                cursor.execute('DELETE FROM aggr_opticalSheetField WHERE idOpticalSheet = ' + str(self.idOpticalSheet))
                cursor.execute('DELETE FROM aggr_survey WHERE idOpticalSheet = ' + str(self.idOpticalSheet))
                cursor.execute('DELETE FROM opticalSheet WHERE idOpticalSheet = ' + str(self.idOpticalSheet))
                cursor.execute('DELETE FROM encoding WHERE idOpticalSheet = ' + str(self.idOpticalSheet))
            else:
                raise OpticalSheetError("Can't delete non saved object.")
        else:
            raise OpticalSheetError('No idOpticalSheet defined.')

