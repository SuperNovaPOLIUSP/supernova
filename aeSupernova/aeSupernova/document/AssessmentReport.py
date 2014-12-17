from AssessmentSubreport import *

class AssessmentReport (AssessmentSubreport):
  
    """
     Base class for all reports. Reports are used to sumarize assessment data about a
     certain course, an academic program or even a whole faculty.
  
    :version:
    :author:
    """
  
    """ ATTRIBUTES
  
     List of subreports that make the different parts of a report object.
  
    subreports  (public)
  
    """
  
    def __init__(self, assessedObject, templateFolder):
        """
         Constructor method.
  
        @param  assessedObject : The target object of an assessment. Could be a course, a class, an academic program, etc.
        @param string templateFolder : Absolute path to the directory where are stored the templates to be used to generate content for the document.
        @return  :
        @author
        """

        super(AssessmentReport, self).__init__(assessedObject, templateFolder)
        self.subreports = []
        pass
  
    def getQuestionnaireFromSubreports(self):
        """
         Gets all the questions from each questionnaire list in the objects subreports,
         without repetition, and stores the resulting list in its own questionnaire
         attirbute. This method basically uses the addQuestionnaire from its parent
         class, adding each subreport questionnaire attribute to its own.
  
        @return  :
        @author
        """
        for subreport in self.subreports:
            self.addQuestionnaire(subreport.questionnaire)
  
    def makeSubreports(self):
        """
         Creat a subreport for each of the elements that must be treated individually
         inside of an assessed object (e.g. a course offer).
  
        @return  :
        @author
        """
        # abstract method
        pass

