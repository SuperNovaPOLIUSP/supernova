from datetime import date

from pulsarInterface.Question import Question
from tools.MySQLConnection import MySQLConnection


class QuestionnaireError(Exception):
    """
     Exception that reports errors during the execution of Questionnaire class methods
  
    :version:
    :author:
    """
    pass

class Questionnaire(object):

    """
     Class representing a set of questions in an assessment.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.
    idQuestionnaire  (private)

     Dictionary of Question objects, in which each key is the question's index in the
     questionnaire and the value is a Question object.
    questions  (private)

     Indicates who or what the questionnaire refers to (usually to a curriculum's
     term).
    description  (private)

     Date on which the questionnaire was created.
    creationDate  (private)

    """

    def __init__(self, questionDictionary, description):
        """
         Constructor method. When creating a questionnaire, this method sets its date to
         the the same as the date of the object's creation.

        @param Question{} questionDictionary : Dictionary of Questions objects, in which each key is the question's index in the questionnaire and the value is a Question object.
        @param string description : Indicates who or what the questionnaire refers to (usually to a curriculum's term).
        @return Questionnaire :
        @author
        """
        if questionDictionary:
            for index in questionDictionary:
                if not isinstance(questionDictionary[index], Question):
                    raise QuestionnaireError('One or more of the entries in questionDictionary is not a question')
        if not isinstance(description, (str, unicode)):
            raise QuestionnaireError('Description must be a string')
        self.questions = questionDictionary
        self.description = description
        self.creationDate = date.today().isoformat()
        self.idQuestionnaire = None

    def __iter__(self):
        """
         Iterator that returns each question of the questionnaire's questions attribute.
        @return Question :
        @author
        """
        if self.questions:
            return self.questions.itervalues()
        else:
            return None  # No questions, no iterator needed

    def __eq__(self, other):
        """
         Comparison method that returns True if two objects of the class Questionnaire
         are equal.
        @param Questionnaire other : Other object of the class Questionnaire to be compared with a present object.
        @author
        """
        if not isinstance(other, Questionnaire):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
         Comparison method that returns True if two objects of the class AnswerType are
         not equal.

        @param Questionnaire other : Other object of the class AnswerType to be compared with a present object.
        @return bool :
        @author
        """
        return not self.__eq__(other)

    def addQuestion(self, question, index):
        """
         Adds a question to the questionnaire's dictionary of questions at the position
         specified by the index parameter. Returns a boolean that confirms if the
         question was successfully added.
        @param Question question : A Question object to be added to the dictionary of questions in the questionnaire.
        @param int index : The index of the question to be inserted in the questionnaire.
        @return bool :
        @author
        """
        if isinstance(question, Question):
            if self.questions:
                try:
                    all_keys = self.questions.keys()
                    allQuestions = self.questions.values()
                    if index in all_keys:
                        return False  # Adding a second question to the same index
                    if question in allQuestions:
                        return False  # Adding a repeated question
                    self.questions[index] = question
                    return True
                except:
                    return False
            else:
                self.questions = {index: question}
                return True
        else:
            return False

    def removeQuestionByIndex(self, index):
        """
         Removes a question, specified by its index, from the questions attribute.
         Returns a boolean that confirms if the question was successfully removed.
        @param int index : Question's index in the questionnaire.
        @return bool :
        @author
        """
        if self.questions:
            try:
                all_keys = self.questions.keys()
                if index not in all_keys:
                    return False  # Key not in dict
                del self.questions[index]
                return True
            except:
                return False
        else:
            return True  # No question removed

    def removeQuestionById(self, idQuestion):
        """
         Removes a question, specified by its database ID, from the questions attribute.
         Returns a boolean that confirms if the question was successfully removed.
        @param int idQuestion : Database ID of the question to be removed from the questionnaire.
        @return bool :
        @author
        """
        question = Question.pickById(idQuestion)
        if self.questions:
            associations = self.questions.items()
            try:
                for association in associations:
                    if association[1] == question:
                        return self.removeQuestionByIndex(association[0])
                return False  # Question not found
            except:
                return False
        else:
            return True  # No question removed

    @staticmethod
    def buildQuestionsQuestionnaire(idOffer):
        """
         Method that returns a list with all the questions from questionnaires that refer to a specific offer.
        @param int idOffer : Database ID of the discipline's offer.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        query = 'select q.idQuestionnaire from questionnaire q, aggr_survey s, aggr_opticalSheetField osf, aggr_offer o where q.idQuestionnaire = s.idQuestionnaire and s.idOpticalSheet = osf.idOpticalSheet and osf.idOffer = o.idOffer and o.idOffer = ' + str(idOffer)
        questionnaire_list = []
        question_list = []
        try:
            results = cursor.execute(query)
            if not results:
                raise QuestionnaireError('Invalid idOffer to build Questionnaire')
            for result in results:
                questionnaire_list.append(Questionnaire.pickById(result[0]))
            for questionnaire in questionnaire_list:
                for question in questionnaire.questions.values():
                    if question not in question_list:
                        question_list.append(question)
            return question_list
        except:
            raise QuestionnaireError('Error joining offer with opticalSheet')

    @staticmethod
    def getQuestionsById(idQuestionnaire):
        """
            Returns a dictionary containing the questions related to a questionnaire's
            id passed as argument

            @param int idQuestionnaire : Database ID of the questionnaire
        """
        cursor = MySQLConnection()
        questions = {}
        query_questions = 'select idQuestion, questionIndex from rel_question_questionnaire where idQuestionnaire = ' + str(idQuestionnaire)
        try:
            search_for_questions = cursor.execute(query_questions)
            if search_for_questions:
                for question_data in search_for_questions:
                    index = question_data[1]
                    question = Question.pickById(question_data[0])
                    questions[index] = question
            return questions
        except:
            raise QuestionnaireError('Error on linking questionnaire to questions')

    @staticmethod
    def pickById(idQuestionnaire):
        """
         Returns a Questionnaire object specified by its database ID.

        @param int idQuestionnaire : Database ID of the questionnaire to be found.
        @return Questionnaire :
        @author
        """
        cursor = MySQLConnection()
        query = 'select description, creationDate from questionnaire where idQuestionnaire = ' + str(idQuestionnaire)
        try:
            result = cursor.execute(query)
            if result:
                questions = Questionnaire.getQuestionsById(idQuestionnaire)
                questionnaire = Questionnaire(questions, result[0][0])
                if result[0][1]:
                    Questionnaire.creationDate = result[0][1].isoformat()
                else:
                    Questionnaire.creationDate = '0000-00-00'
                questionnaire.idQuestionnaire = idQuestionnaire
                return questionnaire
            else:
                return None
        except:
            raise QuestionnaireError('Error on creating new Questionnaire object')

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
         > idQuestionnaire
         > description_equal or description_like
         > creationDate_equal or creationDate_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Questionnaire.find(description_like = "3rdYear", creationDate_equal =
         "2013-01-01", assessmentNumber = 1)

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        questionnairesData = cursor.find('SELECT idQuestionnaire, description, creationDate FROM questionnaire',kwargs)
        questionnaires = []
        for questionnaireData in questionnairesData:
            idQuestionnaire = questionnaireData[0]
            questionnaire = Questionnaire(Questionnaire.getQuestionsById(idQuestionnaire), questionnaireData[1])
            questionnaire.idQuestionnaire = idQuestionnaire
            if questionnaireData[2]:
                questionnaire.creationDate = questionnaireData[2].isoformat()
            else:
                questionnaire.creationDate = '0000-00-00'
            questionnaires.append(questionnaire)
        return questionnaires

    def store(self):
        """
         Stores the data of the Questionnaire object on the database.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        if self.idQuestionnaire:
            # Remove all relations of questions from this questionnaire
            deleteQuery = "delete from rel_question_questionnaire where idQuestionnaire = " + str(self.idQuestionnaire)
            updateQuery = "update questionnaire set description = '" + self.description + "', creationDate = '" + self.creationDate + "'" + ' where idQuestionnaire = ' + str(self.idQuestionnaire)
            cursor.execute(deleteQuery)
            cursor.execute(updateQuery)
        else:
            possibleMatch = Questionnaire.find(description_equal=self.description, creationDate_equal=self.creationDate)
            if possibleMatch:
                self.idQuestionnaire = possibleMatch[0].idQuestionnaire
            else:
                insertQuery = "insert into questionnaire (description, creationDate) values ('" + self.description + "', '" + self.creationDate + "')"
                cursor.execute(insertQuery)
                self.idQuestionnaire = Questionnaire.find(description_equal=self.description, creationDate_equal=self.creationDate)[0].idQuestionnaire
        if self.questions:
            for questionIndex in self.questions:
                insertRelQuestionQuery = 'insert into rel_question_questionnaire values ('
                idQuestionnaire = str(self.idQuestionnaire)
                idQuestion = str(self.questions[questionIndex].idQuestion)
                relationAlreadyStored = cursor.execute('select * from rel_question_questionnaire where idQuestionnaire = ' + idQuestionnaire + ' and idQuestion = ' + idQuestion + ' and questionIndex = ' + str(questionIndex))
                if not relationAlreadyStored:
                    insertRelQuestionQuery += idQuestionnaire + ', ' + idQuestion + ', ' + str(questionIndex) + ')'
                    cursor.execute(insertRelQuestionQuery)

    def delete(self):
        """
         Deletes the data of the Questionnaire object on the database.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        idQuestionnaire = str(self.idQuestionnaire)
        query = 'delete from questionnaire where idQuestionnaire = ' + idQuestionnaire
        query_rel = 'delete from rel_question_questionnaire where idQuestionnaire = ' + idQuestionnaire
        query_rel2 = 'delete from aggr_survey where idQuestionnaire = ' + idQuestionnaire
        cursor.execute(query_rel)
        cursor.execute(query_rel2)
        cursor.execute(query)
