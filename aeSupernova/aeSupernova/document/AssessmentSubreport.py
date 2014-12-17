from Document import *
from pulsarInterface.Question import *

class AssessmentSubreportError(Exception):
    """
     Exception reporting an error in the execution of an AssessmentSubreport operation.

    :version:
    :author:
    """
    pass

class AssessmentSubreport (Document):
  
    """
     Base class for all subreports. Subreports should be used to make the different
     parts of a report, sumarizing data from the assessment of single classes inside
     a course report, for example. Therefore, they represent only data structures and
     should not be used to render templates or wirte documents. Instead, they must be
     used by reports for the renderization of templates and the writing of documents.
  
    :version:
    :author:
    """
  
    """ ATTRIBUTES
  
     The target object of an assessment. Could be a course, a class, an academic
     program, etc.
  
    assessedObject  (public)
  
     Dictionary of charts that represent the answers to each question in the
     assessment. The dictionary follows the format {question : chart}.
  
    charts  (public)
  
     List of questions used in the assessment that will be sumarized by the report.
  
    questionnaire  (public)
  
    """
  
    def __init__(self, assessedObject, templateFolder):
        """
         Constructor method.
  
        @param  assessedObject : The target object of an assessment. Could be a course, a class, an academic program, etc.
        @param string templateFolder : Absolute path to the directory where are stored the templates to be used to generate content for the document.
        @return  :
        @author
        """
        super(AssessmentSubreport, self).__init__(templateFolder)
        self.assessedObject = assessedObject
        self.questionnaire = []
        self.charts = {}
  
    def addQuestionnaire(self, questionnaire):
        """
         Adds a list of questions to the object's list of questions. Does not repeat any
         question.
  
        @param [] questionnaire : List of question objects to be added to the object's questionnaire attribute.
        @return  :
        @author
        """
        if not questionnaire:
            return
        if not isinstance(questionnaire, list):
            raise AssessmentSubreportError("Invalid questionnaire parameter: must be a list.")
        elif not isinstance(questionnaire[0], Question):
            raise AssessmentSubreportError("Invalid questionnaire parameter: must be a list of Question objects.")
  
        # creates a new list containing only questions that are not present in the questionnaire attribute
        newQuestionnaireWithoutRepetitions = []
        for newQuestion in questionnaire:
            repeatedQuestion = False
            for question in self.questionnaire:
                if question == newQuestion:
                    repeatedQuestion = True
  
            if repeatedQuestion:
                continue
            else:
                newQuestionnaireWithoutRepetitions.append(newQuestion)
  
        # extends the existing questionnaire list with the one recently created
        self.questionnaire.extend(newQuestionnaireWithoutRepetitions)
      
    def countAnswers(self):
        """
         Returns a dictionary in the format {question : answers} that stores the answers
         of each question of an assessment.
  
        @return {} :
        @author
        """
        # abstract method
        pass
  
    def generateCharts(self):
        """
         Generates bar charts from the answers stored in the assessmentResults attirbute.
         Stores the charts generated in the charts attirbute.
  
        @return  :
        @author
        """
        # abstract method
        pass
  
