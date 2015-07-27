from tools.MySQLConnection import MySQLConnection


class AnswerError(Exception):
    """
     Exception reporting an error in the execution of an Answer method.

    :version:
    :author:
    """
    pass


class Answer(object):

    """
     Class representing an answer to a question related to a course.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idAnswer  (public)

     Question to which the answer has been given.

    question  (public)

     Associated database key of the related datafile.

    idDatafile  (public)

     The alternative corresponding to a multiple choice question answer. Its values
     must be:
     'A', 'B', 'C', 'D', 'E' or 'X'.

    alternative  (public)

     Identification of an optical sheet, relating it to a line of a datafile.

    identifier  (public)

     The position (column) in the optical sheet.

    courseIndex  (public)

     Represents the code refering to the offer of a course OR a class number in case
     of a non-encoded optical sheet.

    code  (public)

    """

    def __init__(self, questionIndex, alternative, identifier):
        """
        @param Question question : Question to which the answer has been given.
        @param char alternative : The alternative corresponding to a multiple choice question answer. Its values must be:
'A', 'B', 'C', 'D', 'E' or 'X'.
        @param int identifier : Identification of an optical sheet, relating it to a line of a datafile.
        @return  :
        @author
        """
        validAlternatives = ['A', 'B', 'C', 'D', 'E', 'X']
        if not isinstance(questionIndex, (int, long)):
            raise AnswerError('Parameter questionIndex must be an int or long')
        if not alternative or not isinstance(alternative, (str, unicode)) or alternative not in validAlternatives:
            raise AnswerError('Must provide a valid alternative')
        if not identifier or not isinstance(identifier, (int, long)):
            raise AnswerError('Must provide a valid identifier')
        self.questionIndex = questionIndex
        self.alternative = alternative
        self.identifier = identifier
        self.idAnswer = None
        self.idDatafile = None
        self.courseIndex = None
        self.code = None

    def setIdDatafile(self, idDatafile):
        """
         Sets the datafile from which the answer comes from through its idDatafile. It
         should only be used by the Datafile class in order to register its answers.

        @param int idDatafile : Associated database key of the related datafile.
        @return  :
        @author
        """
        if not idDatafile or not isinstance(idDatafile, (int, long)):
            raise AnswerError('Must provide a valid idDatafile')
        self.idDatafile = idDatafile

    def setCode(self, code):
        """
         Set the code for the course assessed, it should only be used if the OpticalSheet
         is coded.

        @return  :
        @author
        """
        if code is None or not isinstance(code, (int, long)):
            raise AnswerError('Must provide a valid code')
        self.code = code

    def setCourseIndex(self, courseIndex):
        """
         Set the courseIndex for the course assessed, it should only be used if the
         OpticalSheet is not coded.

        @return  :
        @author
        """
        if not courseIndex or not isinstance(courseIndex, (int, long)):
            raise AnswerError('Must provide a valid courseIndex')
        self.courseIndex = courseIndex
        
    @staticmethod
    def countAnswers(**kwargs):
        """
         Searches the database and counts the ocurrences of answers matching the
         description specified through the method's parameters.
         
         Returns:
         A dictionary in the format {'A' : 13, 'B' : '27', 'C' : 30, 'D' : 48, 'E' : 5,
         'X' : 62}, which displays the number of answers counted according to the
         alternative.
         
         The parameters admitted to specify the description of the answers to be counted
         are the following:
         > question
         > timePeriod
         > cycle
         > course
         > classNumber
         > professor
         > opticalSheet
         > assessmentNumber
         > datafile
         E. g. Answer.countAnswers(question = questionObject, timePeriod =
         timePeriodObject, course = courseObject)

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return {} :
        @author
        """
        cursor = MySQLConnection()
        #query = 'select a.alternative, count(a.alternative) from answer a'
        #queryComplement = ' where '
        #linkComplements = set([])
        #joinComplements = set([])
        #offerBranchFlag = False
        #linkOffer = 'aggr_offer o'
        #joinOpticalSheetOpticalSheetField = 'os.idOpticalSheet = osf.idOpticalSheet'
        #joinOfferOpticalSheet = 'rco.idOpticalSheet = os.idOpticalSheet'
        #joinOfferOpticalSheetField = 'o.idOffer = osf.idOffer'
        #joinOpticalSheetFieldRel = 'osf.idOpticalSheetField = r.idOpticalSheetField'
        #joinRelAnswer = 'r.idAnswer = a.idAnswer'
        #if 'question' in kwargs:
        #    linkComplements.add('question q')
        #    joinComplements.add(' a.idQuestion = q.idQuestion and q.idQuestion = ' + str(kwargs['question'].idQuestion))
        #if 'timePeriod' in kwargs:
        #    linkComplements.add('timePeriod tp')
        #    linkComplements.add(linkOffer)
        #    joinComplements.add(' tp.idTimePeriod = o.idTimePeriod and tp.idTimePeriod = ' + str(kwargs['timePeriod'].idTimePeriod))
        #    offerBranchFlag = True
        #if 'cycle' in kwargs:
        #    linkComplements.add('cycle c')
        #    linkComplements.add('rel_cycle_opticalSheet rco')
        #    linkComplements.add('opticalSheet os')
        #    linkComplements.add('rel_answer_opticalSheetField_survey r')
        #    linkComplements.add('aggr_opticalSheetField osf')
        #    joinComplements.add(' c.idCycle = rco.idCycle and c.idCycle = ' + str(kwargs['cycle'].idCycle))
        #    joinComplements.add(joinOfferOpticalSheet)
        #    joinComplements.add(joinOpticalSheetOpticalSheetField)
        #    joinComplements.add(joinOpticalSheetFieldRel)
        #    joinComplements.add(joinRelAnswer)
        #if 'course' in kwargs:
        #    linkComplements.add('course co')
        #    linkComplements.add(linkOffer)
        #    joinComplements.add(' co.idCourse = o.idCourse and co.idCourse = ' + str(kwargs['course'].idCourse))
        #    offerBranchFlag = True
        #if 'offer_byClass' in kwargs:
        #    linkComplements.add(linkOffer)
        #    joinComplements.add(' o.classNumber = ' + str(kwargs['offer_byClass']))
        #    offerBranchFlag = True
        #if 'offer_byProfessor' in kwargs:
        #    linkComplements.add(linkOffer)
        #    joinComplements.add(' o.idProfessor = ' + str(kwargs['offer_byProfessor']))
        #    offerBranchFlag = True
        #if offerBranchFlag:
        #    linkComplements.add('aggr_opticalSheetField osf')
        #    linkComplements.add('rel_answer_opticalSheetField_survey r')
        #    joinComplements.add(joinOfferOpticalSheetField)
        #    joinComplements.add(joinOpticalSheetFieldRel)
        #    joinComplements.add(joinRelAnswer)
        #for linkComplement in linkComplements:
        #    query += ', '
        #    query += linkComplement
        #for complement in joinComplements:
        #    queryComplement += complement
        #    queryComplement += ' and '
        #queryComplement = queryComplement[:-5]
        #query += queryComplement + ' group by a.idAnswer'
        parameters = ''
        if 'question' in kwargs.keys():
            parameters = parameters + ' rel_question_questionnaire.idQuestion = ' + str(kwargs['question'].idQuestion) + ' AND'
        if 'datafile' in kwargs.keys():
            parameters = parameters + ' answer.idDatafile = ' + str(kwargs['datafile'].idDatafile) +' AND'
        if 'timePeriod' in kwargs.keys():
            parameters = parameters + ' aggr_offer.idTimePeriod = ' + str(kwargs['timePeriod'].idTimePeriod) + ' AND'
        if 'cycle' in kwargs.keys():
            parameters = parameters + ' rel_cycle_opticalSheet.idCycle = ' + str(kwargs['cycle'].idCycle) + ' AND'
        if 'course' in kwargs.keys():
            parameters = parameters + ' aggr_offer.idCourse = ' + str(kwargs['course'].idCourse) + ' AND'
        if 'professor' in kwargs.keys():
            parameters = parameters + ' aggr_offer.idProfessor = ' + str(kwargs['professor'].idProfessor) + ' AND'
        if 'classNumber' in kwargs.keys():
            parameters = parameters + ' aggr_offer.classNumber = ' + str(kwargs['classNumber']) + ' AND'
        if 'opticalSheet' in kwargs.keys():
            parameters = parameters + ' aggr_opticalSheetField.idOpticalSheet = ' + str(kwargs['opticalSheet'].idOpticalSheet) + ' AND'
        if 'assessmentNumber' in kwargs.keys():
            parameters = parameters + ' aggr_survey.assessmentNumber = ' + str(kwargs['assessmentNumber']) + ' AND'
        if parameters != '':
            parameters = parameters[:-4]
        query = 'SELECT answer.alternative FROM answer JOIN rel_answer_opticalSheetField_survey ON rel_answer_opticalSheetField_survey.idAnswer = answer.idAnswer JOIN aggr_opticalSheetField ON aggr_opticalSheetField.idOpticalSheetField = rel_answer_opticalSheetField_survey.idOpticalSheetField JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer  JOIN aggr_survey ON aggr_survey.idSurvey = rel_answer_opticalSheetField_survey.idSurvey JOIN rel_question_questionnaire ON aggr_survey.idQuestionnaire = rel_question_questionnaire.idQuestionnaire AND rel_question_questionnaire.questionIndex = answer.questionIndex JOIN rel_cycle_opticalSheet ON rel_cycle_opticalSheet.idOpticalSheet = aggr_opticalSheetField.idOpticalSheet WHERE '+parameters+' GROUP BY answer.idAnswer'
        mainQuery = 'select b.alternative, count(*) from (' + query + ') b group by b.alternative'
        answers = {'A' : 0, 'B' : 0, 'C' : 0, 'D' : 0, 'E' : 0, 'X' : 0}
        searchData = cursor.execute(mainQuery)
        if searchData:
            for data in searchData:
                answers[str(data[0])] = data[1]
        if 'A' not in answers.keys():
            answers['A'] = 0
        if 'B' not in answers.keys():
            answers['B'] = 0
        if 'C' not in answers.keys():
            answers['C'] = 0
        if 'D' not in answers.keys():
            answers['D'] = 0
        if 'E' not in answers.keys():
            answers['E'] = 0
        if 'X' not in answers.keys():
            answers['X'] = 0
        return answers

    @staticmethod
    def pickById(idAnswer):
        """
         Returns one complete Answer object where its ID is equal to the chosen.

        @param int idAnswer : Associated database key.
        @return Answer :
        @author
        """
        cursor = MySQLConnection()
        query = 'SELECT questionIndex, idDatafile, alternative, identifier FROM answer WHERE idAnswer = ' + str(idAnswer)
        searchData = cursor.execute(query)
        if searchData:
            questionIndex = searchData[0][0]
            idDatafile = searchData[0][1]
            alternative = searchData[0][2]
            identifier = searchData[0][3]
            answer = Answer(questionIndex, alternative, identifier)
            answer.idAnswer = idAnswer
            answer.setIdDatafile(idDatafile)
            return answer
        raise AnswerError('Answer not found')

    @staticmethod
    def find(**kwargs):
        """
         Searches the database to find one or more objects that fit the description
         specified by the method's parameters. It is possible to perform two kinds of
         search when passing a string as a parameter: a search for the exact string
         (EQUAL operator) and a search for at least part of the string (LIKE operator).
         
         Returns:
         A list of objects that match the specifications made by one (or more) of the
         folowing parameters:
         > idAnswer
         > question
         > questionIndex
         > idDataFile
         > alternative
         > identifier
         
         E. g. Answer.find(question = questionObject, identifier = 21, idDataFile = 413)

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return Answer[] :
        @author
        """
        cursor = MySQLConnection()
        answers = []
        complement = ''
        if 'question' in kwargs:
            kwargs['idQuestion'] = kwargs['question'].idQuestion
            complement = ' JOIN rel_answer_opticalSheetField_survey ON rel_answer_opticalSheetField_survey.idAnswer = answer.idAnswer JOIN aggr_survey ON aggr_survey.idSurvey = rel_answer_opticalSheetField_survey.idSurvey JOIN rel_question_questionnaire ON rel_question_questionnaire.idQuestionnaire = aggr_survey.idQuestionnaire'
            del(kwargs['question'])
        if 'alternative' in kwargs:
            alt = kwargs['alternative']
            del(kwargs['alternative'])
            kwargs['alternative_equal'] = alt
        if 'idAnswer' in kwargs:
            kwargs['answer.idAnswer'] = kwargs['idAnswer']
            del(kwargs['idAnswer'])
        query = 'SELECT answer.idAnswer, answer.questionIndex, idDatafile, alternative, identifier FROM answer ' + complement
        searchData = cursor.find(query, kwargs)
        if searchData:
            for answerData in searchData:
                questionIndex = answerData[1]
                alternative = answerData[3]
                identifier = answerData[4]
                idDatafile = answerData[2]
                answer = Answer(questionIndex, alternative, identifier)
                answer.idAnswer = answerData[0]
                answer.setIdDatafile(idDatafile)
                answers.append(answer)
        return answers
