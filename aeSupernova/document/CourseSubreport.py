from AssessmentSubreport import *
from BarChart import *

from multiprocessing import Process, JoinableQueue # package for implementing multiprocessing tasks

# pulsarInterface basic layer
from pulsarInterface.TimePeriod import * # Class from the pulsarInterface package that allows manipulation of time period data
from pulsarInterface.Answer import * # Class from the pulsarInterface package that allows manipulation of answer data
from pulsarInterface.Offer import * # Class from the pulsarInterface package that allows manipulation of course offer data
from pulsarInterface.Questionnaire import * # Class from the pulsarInterface package that allows manipulation of questionnaire data
from pulsarInterface.Question import * # Class from the pulsarInterface package that allows manipulation of questionnaire data

class CourseSubreportError(Exception):
    """
     Exception reporting an error in the execution of a CourseSubreport operation.

    :version:
    :author:
    """
    pass

class CourseSubreport (AssessmentSubreport):
  
    """
     Class that models a course subreport, which comprehends the data analysis charts
     representing the answers obtained through the assessment, in a certain time
     period, of a course class or of a course offer.

    :version:
    :author:
    """

    """ ATTRIBUTES
  
     Boolean that marks if the course subreport should be made by class
     number or by professor.     
  
    reportByClass  (public)

     Integer that indicates the number of the assessment to which the
     answers that must be counted were given.
  
    assessmentNumber  (public)
  
    """

    def __init__(self, assessedObject, templateFolder, reportByClass):
        """
         Constructor method.
  
        @param  assessedObject : The target object of an assessment. Could be a course, a class, an academic program, etc.
        @param string templateFolder : Absolute path to the directory where are stored the templates to be used to generate content for the document.
        @return  :
        @author
        """
        super(CourseSubreport, self).__init__(assessedObject, templateFolder)
        self.assessmentNumber = 1
        self.reportByClass = reportByClass
  
    def countAnswers(self):
        """
         Implements the abstract method from superclass in order to count answers for
         course offers or course classes.
         Returns a dictionary in the format {question : answers} that stores the answers
         of each question of an assessment.
  
        @return {} :
        @author
        """
        answers = {}
        """# Function defined to count answers through multiprocessing:
        def makeAnswerCount(queue, question):
            if self.reportByClass:
                # counts answers by class number
                countedAnswer = Answer.countAnswers(question = question, timePeriod = self.assessedObject.timePeriod, course = self.assessedObject.course, classNumber = self.assessedObject.classNumber, assessmentNumber = self.assessmentNumber)
            else:
                # counts answers by professor
                countedAnswer = Answer.countAnswers(question = question, timePeriod = self.assessedObject.timePeriod, course = self.assessedObject.course, professor = self.assessedObject.professor, assessmentNumber = self.assessmentNumber)
            
            # inserts counted answers in multiprocessing queue
            if not queue.full():
                queue.put((question, countedAnswer))
        # End of function makeAnswerCount definition                """
        questions = Questionnaire.buildQuestionsQuestionnaire(self.assessedObject.idOffer)
        self.questionnaire = questions
        for question in self.questionnaire:
            if self.reportByClass:
                # counts answers by class number
                countedAnswer = Answer.countAnswers(question = question, timePeriod = self.assessedObject.timePeriod, course = self.assessedObject.course, classNumber = self.assessedObject.classNumber, assessmentNumber = self.assessmentNumber)
            else:
                # counts answers by professor
                countedAnswer = Answer.countAnswers(question = question, timePeriod = self.assessedObject.timePeriod, course = self.assessedObject.course, professor = self.assessedObject.professor, assessmentNumber = self.assessmentNumber)
            if hasAnswers(countedAnswer):
                answers[question.idQuestion] = countedAnswer
        return answers


        """# answer counting through multiprocessing
        queue = JoinableQueue()

        for question in self.questionnaire:
            process = Process(target = makeAnswerCount, args = (queue, question,))
            process.start()

        # Gets answers from multiprocessing queue
        queue.join()

        for question in self.questionnaire:
            queueObject = queue.get()
            answers[queueObject[0].idQuestion] = queueObject[1] """

 
    def generateCharts(self):
        """
         Implements the abstract method from superclass in order to generate charts for
         course offers or course classes.
         Generates charts from the answers stored in the assessmentResults attribute.
         Stores the charts generated in the charts attribute (described in the superclass
         documentation).
  
        @return  :
        @author
        """
        self.questionnaire = Questionnaire.buildQuestionsQuestionnaire(self.assessedObject.idOffer)
        answers = self.countAnswers()
        self.questionnaire = [question for question in self.questionnaire if answers.has_key(question.idQuestion)]
        for question in self.questionnaire:
            data = answers[question.idQuestion]
            dataLabels = question.answerType.alternativeMeaning
            directoryPath = self.texSource.directoryPath
            fileName = "chart_q" + str(question.idQuestion) + "_" + str(id(self))
            chart = BarChart(data, dataLabels, directoryPath, fileName)
            self.charts[question.idQuestion] = chart

        """# Function defined to generate a chart through multiprocessing:
        def makeChart(queue, question, data, dataLabels, directoryPath, fileName):
            chart = BarChart(data, dataLabels, directoryPath, fileName)
            if not queue.full():
                queue.put((question, chart))
        # End of function makeChart definition

        # Chart generation through multiprocessing
        queue = JoinableQueue()"""

        """for question in self.questionnaire:
            process = Process(target = makeChart, args = (queue, question, answers[question.idQuestion], question.answerType.alternativeMeaning, self.texSource.directoryPath, "chart_q" + str(question.idQuestion) + "_" + str(id(self)), ))
            process.start()"""

        """# Gets charts from multiprocessing queue
        queue.join()
        
        for question in self.questionnaire:
            queueObject = queue.get()
            self.charts[queueObject[0].idQuestion] = queueObject[1]"""

    def setReportInstructions(self, assessmentNumber = 1, reportByClass = True):
        """
         Constructor method.
  
        @param int assessmentNumber : Integer that indicates the number of the assessment to which the answers that must be counted were given.
        @param bool reportByClass : Boolean that marks if the course subreport should be made by class number or by professor.
        @return  :
        @author
        """
        # checks validity of assessmentNumber parameter
        if not isinstance(assessmentNumber, int):
            raise CourseSubreportError("Invalid assessmentNumber parameter: must be an integer.")
        elif assessmentNumber < 1:
            raise CourseSubreportError("Invalid assessmentNumber parameter: must be an integer greater than 1.")

        # checks validity of reportByClass parameter            
        if not isinstance(reportByClass, bool):
            raise CourseSubreportError("Invalid reportByClass parameter: must be a boolean.")

        self.assessmentNumber = assessmentNumber
        self.reportByClass = reportByClass


def hasAnswers(answerDict):
    """Returns true if the dictionary has at least 1 answer"""
    for key in answerDict:
        if answerDict[key] > 0:
            return True
    return False
