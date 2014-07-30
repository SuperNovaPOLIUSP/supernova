#encoding: utf8
from pulsarInterface.Answer import Answer
from pulsarInterface.Course import Course
from pulsarInterface.Cycle import Cycle
from pulsarInterface.Offer import Offer
from pulsarInterface.OpticalSheet import OpticalSheet, OpticalSheetError
from pulsarInterface.Question import Question
from pulsarInterface.Questionnaire import Questionnaire
from pulsarInterface.TimePeriod import TimePeriod
from tools.MySQLConnection import MySQLConnection


class OpticalSheetController(object):

    """
     

    :version:
    :author:
    """
    @staticmethod
    def findOpticalSheetById(idOpticalSheet):
        """
         Returns the getOpticalSheetData with the opticalSheet of the given id.

        @param int idOpticalSheet : The database id of the wanted opticalSheet
        @return  :
        @author
        """
        opticalSheet = OpticalSheet.pickById(idOpticalSheet)
        if opticalSheet == None:
            return len(opticalSheet)
        return OpticalSheetController.getOpticalSheetData(opticalSheet)

    @staticmethod
    def findOpticalSheetByTimePeriod_Cycle_Term(idTimePeriod, idCycle, term):
        """
         Returns the getOpticalSheetData of the opticalSheet belonging to the given
         idTimePeriod, idCycle and term. If the number of opticalSheets found by those
         parameters is different than 1 the return is the number of opticalSheets found.

        @param int idTimePeriod : The database id of the timePeriod of the wanted opticalSheet.
        @param int idCycle : The database id of the cycle of the wanted opticalSheet.
        @param int term : The term of the wanted opticalSheet.
        @return [] :
        @author
        """
        opticalSheet = OpticalSheet.find(timePeriod = TimePeriod.pickById(idTimePeriod), cycles = [Cycle.pickById(idCycle)], term = term)
        if len(opticalSheet) != 1:
            return len(opticalSheet)
        opticalSheet = opticalSheet[0]
        return OpticalSheetController.getOpticalSheetData(opticalSheet)


    @staticmethod
    def getOpticalSheetData(opticalSheet):
        """
         Returns a dictionary with all the information needed to build and opticalSheet
         in the opticalSheet's site

        @param OpticalSheet opticalSheet : 
        @return {} :
        @author
        """
        opticalSheetDict = {}  
        opticalSheetDict['idOpticalSheet'] = opticalSheet.idOpticalSheet
        opticalSheetDict['surveyType'] = opticalSheet.surveyType
        opticalSheetDict['surveys'] = []
        for survey in opticalSheet.surveys:
            surveyDict = {}
            surveyDict['assessmentNumber'] = survey.assessmentNumber
            surveyDict['idQuestionnaire'] = survey.questionnaire.idQuestionnaire
            surveyDict['questions'] = []
            for questionIndex in survey.questionnaire.questions:
                questionDict = {}
                questionDict['questionIndex'] = questionIndex
                question = survey.questionnaire.questions[questionIndex]
                questionDict['questionWording'] = question.questionWording
                questionDict['idQuestion'] = question.idQuestion
                questionDict['idAnswerType'] = question.answerType.idAnswerType
                surveyDict['questions'].append(questionDict)
            opticalSheetDict['surveys'].append(surveyDict) 
        if opticalSheet.encodingName == None: #If the opticalSheet is not encoded.
            opticalSheet.fillOpticalSheetFields()
            offersSet = {} #First group them by courseIndex.
            for field in opticalSheet.fields:
                if not field.courseIndex in offersSet.keys():
                    offersSet[field.courseIndex] = []
                offersSet[field.courseIndex].append(field.offer)
            opticalSheetDict['fields'] = [] #Now get the wanted informations.
            for courseIndex in offersSet:
                complement = Offer.offersName([offersSet[courseIndex]])[0]
                fieldDict = {}
                fieldDict['courseIndex'] = courseIndex
                fieldDict['idsOffer'] = [offer.idOffer for offer in offersSet[courseIndex]]
                fieldDict['courseCode'] = offersSet[courseIndex][0].course.courseCode + complement
                fieldDict['courseAbbreviation'] = offersSet[courseIndex][0].course.abbreviation + complement
                fieldDict['courseName'] = offersSet[courseIndex][0].course.name + complement
                fieldDict['idCourse'] = offersSet[courseIndex][0].course.idCourse
                opticalSheetDict['fields'].append(fieldDict)
        else:
            opticalSheetDict['encodingName'] = opticalSheet.encodingName
        return opticalSheetDict

    @staticmethod 
    def getOldOpticalSheets(idCycle):
        """
         Returns the a dict with the idOpticalSheet, the term and the TimePeriod string of the existing
         opticalSheets relatade to this cycle.

        @param Cycle cycle : The cycle related to the wanted opticalSheets
        @return  :
        @author
        """
        cursor = MySQLConnection()
        opticalSheets = cursor.execute('SELECT aggr_opticalSheetField.idOpticalSheet, rel_cycle_opticalSheet.term, aggr_offer.idTimePeriod FROM rel_cycle_opticalSheet JOIN aggr_opticalSheetField ON rel_cycle_opticalSheet.idOpticalSheet = aggr_opticalSheetField.idOpticalSheet JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer WHERE rel_cycle_opticalSheet.idCycle = ' + str(idCycle) + ' GROUP BY aggr_opticalSheetField.idOpticalSheet ORDER BY aggr_offer.idTimePeriod DESC;')
        response = []
        for opticalSheet in opticalSheets:
            opticalSheetDict = {}
            opticalSheetDict['term'] = opticalSheet[1]
            opticalSheetDict['timePeriod'] = str(TimePeriod.pickById(opticalSheet[2]))
            opticalSheetDict['idOpticalSheet'] = opticalSheet[0]
            response.append(opticalSheetDict)
        return response
    

        
    
    @staticmethod
    def storeOpticalSheet(idOpticalSheet, surveyType, idCycle, term, idTimePeriod, fields, surveys, encoded):
        """
         Tries to store the opticalSheet and returns a mensage explaning what happend.

        @param int idOpticalSheet : Id of the opticalSheet to be store, if it is a new one it should be None.
        @param string surveyType : A string defining the type of the opticalSheets survey, must be in minitableSurveyType.
        @param int idCycle : The database id of the cycle to be added in this opticalSheet, it can't be None, it is ok if this cycle is alredy related to this opticalSheet.
        @param int term : Term to be added in the relation cycle opticalSheet .
        @param int idTimePeriod : Database id of the timePeriod in which this opticalSheet exist.
        @param [] fields : If not encoded: A list of dicts, where each dict represent a field and contain the keys: idsOffer, courseIndex, abbreviation, idCourse.
                           Else is just the encoding name
        @param [] surveys : A list of dicts where each dict represents a survey with the keys: 
assessmentNumber, 
idQuestionnaire: None or the IdQuestionnaire,
questions: [{questionWording, questionIndex}
        @param string encoded : A boolean to define if this opticalSheet is encoded
        @return  string:
        @author
        """
        timePeriod = TimePeriod.pickById(idTimePeriod)
        cycle = Cycle.pickById(idCycle)
        storedFields = False
        storedQuestionnaire = False
        if idOpticalSheet != None:
            opticalSheet = OpticalSheet.pickById(idOpticalSheet)
            if opticalSheet.surveyType != surveyType:
                raise OpticalSheetError("ERROR: Given surveyType is different than opticalSheet's surveyType.")
            #clear opticalSheets surveys
            opticalSheet.surveys = []
        else:
            #Before creating a new one check if it already exist
            if encoded:
                if len(OpticalSheet.find(encodingName = fields)) > 0:
                    raise OpticalSheetError("There can only be one opticalSheet per encoding!")
            if len(OpticalSheet.find(cycles = [cycle], term = term, timePeriod = timePeriod)) > 0: #Even encoded opticalSheets have to pass through this
                raise OpticalSheetError("There can be only one opticalSheet per cycle, term and timePeriod")
            #Now it is ok to store
            opticalSheet = OpticalSheet(surveyType)
            if encoded:
                opticalSheet.setEncodingName(fields)
            opticalSheet.store()
        hasAnswers = False
        answers = Answer.countAnswers(opticalSheet = opticalSheet)
        for key in answers:
            if answers[key] > 0:
                hasAnswers = True
        if not hasAnswers: #Can't alter offers with answers
            #First deal with the fields
            if not encoded:
                for field in fields:
                    idsOffer = [int(offer) for offer in field['idOffers']]
                    if len(idsOffer) > 0:
                        course = Course.pickById(field['idCourse'])
                        abbreviation = field['abbreviation'].split('(')[0].split('[')[0]
                        course.setAbbreviation(abbreviation)
                        course.store()
                        opticalSheet.addOpticalSheetField(Offer.find(idOffer = idsOffer), int(field['courseIndex']) + 1)
                    else:
                        opticalSheet.removeOpticalSheetField(int(field['courseIndex']) + 1)
                    print field['courseIndex']
            storedFields = True
        #Next the cycle
        if not {'term':term, 'cycle':cycle} in opticalSheet.cycles:
            opticalSheet.addCycle_Term(cycle, term)

        for survey in surveys:
            hasAnswers = False
            answers = Answer.countAnswers(opticalSheet = opticalSheet, assessmentNumber = survey['assessmentNumber'])
            for key in answers:
                if answers[key] > 0:
                    hasAnswers = True
            if not hasAnswers: #Can't alter a survey with answers
                #prepare the questionDict
                questionDict = {}
                for questionData in survey['questions']:
                    if questionData['idQuestion'] != None:
                        question = Question.pickById(questionData['idQuestion'])
                        questionDict[int(questionData['questionIndex']) + 1] = question
                #Create or find the questionnaire
                if survey['idQuestionnaire'] != None:
                    questionnaire = Questionnaire.pickById(survey['idQuestionnaire'])
                    #If the questionnaire exist update its questions
                    if questionnaire.questions != questionDict:
                        questionnaire.questions = questionDict
                        questionnaire.store()
                else:
                    #Create it
                    if encoded: #this is only to know the questionnaire's discription
                        questionnaire = Questionnaire(questionDict, fields + str(timePeriod))
                    else:
                        questionnaire = Questionnaire(questionDict, cycle.name + '-' + str(term) + '-' + str(timePeriod))
                    questionnaire.store()
                #Now remove old survey of this assessment in this opticalSheet (this method works even if there are no surveys in this opticalSheet)
                opticalSheet.removeSurvey(survey['assessmentNumber'])
                opticalSheet.addSurvey(questionnaire, survey['assessmentNumber'])                        
                storedQuestionnaire = True
        if storedQuestionnaire or storedFields:
            opticalSheet.store()
        if storedFields:
            return 'OpticalSheet was stored'
        elif storedQuestionnaire:
            return 'Only Questionnaire was stored'
        else:
            raise OpticalSheetError("Can't save a opticalSheet with answers in the same assessment!!")

