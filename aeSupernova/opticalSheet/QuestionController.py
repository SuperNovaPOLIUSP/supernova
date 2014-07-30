from pulsarInterface.AnswerType import AnswerType
from pulsarInterface.Question import Question

class QuestionController(object):

    """
     

    :version:
    :author:
    """
    
    @staticmethod
    def findQuestion(partialQuestionWording):
        """
         Returns the questions in which the questionWording contain the chosen
         partialQuestionWording. The return is a list of dicts with the keys:
         questionWording, idQuestion, idAnswerType and answerTypeName

        @param string partialQuestionWording : Part of the wanted question wording.
        @return  :
        @author
        """
        questions = Question.find(questionWording_like = partialQuestionWording)
        finalList = []
        for question in questions:
            questionDict = {}
            questionDict['questionWording'] = question.questionWording
            questionDict['idQuestion'] = question.idQuestion
            questionDict['idAnswerType'] = question.answerType.idAnswerType
            questionDict['answerTypeName'] = question.answerType.name
            finalList.append(questionDict)
        return finalList

    @staticmethod
    def getAnswerTypes():
        """
         Returns all the answerTypes in the database as a list of dict with the keys as
         it is defined in AnswerType class: idAnswerType, answerTypeName,
         alternativeMeaning

        @return [] :
        @author
        """
        answerTypes = AnswerType.find()
        finalList = []
        for answerType in answerTypes:
            answerTypeDict = {}
            answerTypeDict['answerTypeName'] = answerType.name
            answerTypeDict['idAnswerType'] = answerType.idAnswerType
            answerTypeDict['alternativeMeaning'] = answerType.alternativeMeaning
            finalList.append(answerTypeDict)
        return finalList

    @staticmethod
    def storeQuestion(idAnswerType, questionWording):
        """
         Stores the given question, and returns its new idQuestion.

        @param int idAnswerType : 
        @param string questionWording : 
        @return  :
        @author
        """
        answerType = AnswerType.pickById(idAnswerType)
        question = Question(questionWording, answerType)
        question.store()
        return question.idQuestion



