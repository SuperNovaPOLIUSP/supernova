from AssessmentReport import *
from CourseSubreport import *
from BarChart import *

from multiprocessing import Process, JoinableQueue # package for implementing multiprocessing tasks

# pulsarInterface basic layer
from pulsarInterface.OpticalSheetField import *
from pulsarInterface.TimePeriod import * # Class from the pulsarInterface package that allows manipulation of time period data
from pulsarInterface.Answer import * # Class from the pulsarInterface package that allows manipulation of answer data
from pulsarInterface.Offer import * # Class from the pulsarInterface package that allows manipulation of course offer data
from pulsarInterface.Faculty import * # Class from the pulsarInterface package that allows manipulation of faculty data
from pulsarInterface.Questionnaire import * # Class from the pulsarInterface package that allows manipulation of questionnaire data

class CourseReportError(Exception):
    """
     Exception reporting an error in the execution of a CourseReport operation.

    :version:
    :author:
    """
    pass

class CourseReport (AssessmentReport):

    """
     Class that models a report that summarizes the results of a course assessment
     made in a certain time period.
  
    :version:
    :author:
    """
  
    """ ATTRIBUTES
  
     Integer that indicates the number of the assessment to which the answers that
     must be counted were given.
  
    assessmentNumber  (public)
  
     TimePeriod object that represents the term and year when the assessment data (to
     be described by the report) was gathered.
  
    assessmentTimePeriod  (public)
  
     The faculty to which the course report is being presented.
  
    faculty  (public)
  
     Boolean that marks if the course subreport should be made by class number or by
     professor.
  
    reportByClass  (public)
  
     Boolean that marks if the report should exhibit the names of the professors
     ahead of the course offers assessed.
  
    showProfessorName  (public)
  
    """
  
    def __init__(self, assessedObject, assessmentTimePeriod, templateFolder):
        """
         Constructor method.
  
        @param  assessedObject : The target object of an assessment. Could be a course, a class, an academic program, etc.
        @param TimePeriod assessmentTimePeriod : TimePeriod object that represents the term and year when the assessment data (to be described by the report) was gathered.
        @param string templateFolder : Absolute path to the directory where are stored the templates to be used to generate content for the document.
        @return  :
        @author
        """
        super(CourseReport, self).__init__(assessedObject, templateFolder)
       
        # checks validity of assessmentTimePeriod parameter
        if not isinstance(assessmentTimePeriod, TimePeriod):
            raise CourseReportError("Invalid assessmentTimePeriod parameter: must be a TimePeriod object.")

        self.assessmentTimePeriod = assessmentTimePeriod

        # initializes other attributes with default values
        self.assessmentNumber = 1
        self.faculty = Faculty.find(abbreviation_equal = "EPUSP")[0]
        self.reportByClass = True
        self.showProfessorName = True
  
    def countAnswers(self):
        """
         Implements the abstract method from superclass in order to count answers for a
         course assessment.
         Returns a dictionary in the format {question : answers} that stores the answers
         of each question of an assessment.
  
        @return {} :
        @author
        """
        
        answers = {}
        for question in self.questionnaire:
            countedAnswer = Answer.countAnswers(question = question, timePeriod = self.assessmentTimePeriod, course = self.assessedObject, assessmentNumber = self.assessmentNumber)
            
            if hasAnswers(countedAnswer):
                answers[question.idQuestion] = countedAnswer
        self.questionnaire = [question for question in self.questionnaire if answers.has_key(question.idQuestion)]
        return answers           

    """
        # Function defined to count answers through multiprocessing:
        def makeAnswerCount(queue, question):
            countedAnswer = Answer.countAnswers(question = question, timePeriod = self.assessmentTimePeriod, course = self.assessedObject, assessmentNumber = self.assessmentNumber)
            
            # inserts counted answers in multiprocessing queue
            if not queue.full():
                queue.put((question, countedAnswer))
        # End of function makeAnswerCount definition

        # answer counting through multiprocessing
        queue = JoinableQueue()

        for question in self.questionnaire:
            process = Process(target = makeAnswerCount, args = (queue, question,))
            process.start()

        # Gets answers from multiprocessing queue
        queue.join()

        for question in self.questionnaire:
            queueObject = queue.get()
            answers[queueObject[0].idQuestion] = queueObject[1]"""
  
    def generateCharts(self):
        """
         Implements the abstract method from superclass in order to generate charts for a
         course assessment.
         Generates charts from the answers stored in the assessmentResults attribute.
         Stores the charts generated in the charts attribute.
  
        @return  :
        @author
        """
        
        # First, generates subreports charts
        for subreport in self.subreports:
            subreport.generateCharts()


        # Finds all of the questions in the report by inspecting its subreports
        self.getQuestionnaireFromSubreports()

        # Counts answers for the course
        courseAnswers = self.countAnswers()

        # Finally, generates course charts
        for question in self.questionnaire:
            data = courseAnswers[question.idQuestion]
            dataLabels = question.answerType.alternativeMeaning
            directoryPath = self.texSource.directoryPath
            fileName = "chart_q" + str(question.idQuestion) + "_" + str(id(self))
            chart = BarChart(data, dataLabels, directoryPath, fileName)
            self.charts[question.idQuestion] = chart

        """
        # Function defined to generate a chart through multiprocessing:
        def makeCourseChart(chartQueue, question, data, dataLabels, directoryPath, fileName):
            chart = BarChart(data, dataLabels, directoryPath, fileName)
            if not chartQueue.full():
                chartQueue.put((question, chart))
        # End of function makeCourseChart definition

        # Chart generation through multiprocessing
        chartQueue = JoinableQueue()

        for question in self.questionnaire:
            process = Process(target = makeCourseChart, args = (chartQueue, question, courseAnswers[question.idQuestion], question.answerType.alternativeMeaning, self.texSource.directoryPath, "chart_q" + str(question.idQuestion) + "_" + str(id(self))))
            process.start()

        # Gets charts from multiprocessing queue
        chartQueue.join()

        for question in self.questionnaire:
            queueObject = chartQueue.get()
            self.charts[queueObject[0].idQuestion] = queueObject[1]"""


    def updateSubreportsQuestionnaires(self):
        for subreport in self.subreports:
            subreport.questionnaire = self.questionnaire

  
    def generateContents(self):
        """
         Implements abstract method from superclass in order to generate the LaTeX source
         code for a course report.
         Generates a string with the contents of the LaTeX source code that will be
         compiled in order to produce the document.
  
        @return  :
        @author
        """
        self.makeSubreports()
        self.updateSubreportsQuestionnaires()
        self.generateCharts()

        # sets template file names
        headerTemplate_fileName = "CourseReport_headerTemplate.tex"
        pageHeaderTemplate_fileName = "CourseReport_pageHeaderTemplate.tex"
        questionTemplate_fileName = "CourseReport_questionTemplate.tex"

        # sets header template parameters
        headerTemplate_parameters = {
            "facultyAbbreviation" : self.faculty.abbreviation,
            "timePeriod" : unicode(self.assessmentTimePeriod),
            "courseCode" : self.assessedObject.courseCode,
            "courseName" : self.assessedObject.name}

        # renders document header
        self.renderFromTemplate(headerTemplate_fileName, headerTemplate_parameters)
        

        # writes LaTeX source code for each of the course reports subreports
        for subreport in self.subreports:

            subreportChartNumber = 3 # keeps track of subreport pages
            subreportPageNumber = 0 # keeps track of the subreport length
            for question in subreport.questionnaire:

                # renders page header from three to three charts
                if subreportChartNumber == 3:
                    # sets page header template parameters
                    pageHeaderTemplate_parameters = {
                        "showProfessorName" : self.showProfessorName,
                        "classNumber" : unicode(subreport.assessedObject.classNumber),
                        "professorName" : subreport.assessedObject.professor.name}
    
                    # renders page header
                    self.renderFromTemplate(pageHeaderTemplate_fileName, pageHeaderTemplate_parameters)

                    subreportChartNumber = 0 # resets chart number after inserting page header
                
                # renders a question and the charts depicting its answers
                questionTemplate_parameters = {
                    "questionWording" : question.questionWording,
                    "totalAnswers" : unicode(subreport.charts[question.idQuestion].getTotalData()),
                    "nullAnswers" : unicode(subreport.charts[question.idQuestion].data['X']),
                    "percentageOfNullAnswers" : subreport.charts[question.idQuestion].getPercentageData()['X'],
                    "alternativeMeaning" : question.answerType.alternativeMeaning,
                    "percentageAnswers" : subreport.charts[question.idQuestion].getPercentageData(),
                    "classNumber" : unicode(subreport.assessedObject.classNumber),
                    "courseCode" : self.assessedObject.courseCode,
                    "offerChart" : "{" + subreport.charts[question.idQuestion].getAbsolutePath() + "}",
                    "courseChart" : "{" + self.charts[question.idQuestion].getAbsolutePath() + "}"}


                self.renderFromTemplate(questionTemplate_fileName, questionTemplate_parameters)

                # inserts new page from three to three charts
                if subreportChartNumber == 2:
                    self.insertNewPage()
                    subreportPageNumber += 1

                subreportChartNumber += 1

            # makes sure that the subreport fits in an even number of pages
            if subreportPageNumber % 2 == 0: # this means odd number of pages
                self.insertNewPage()

            # inserts new page at the end of a subreport (only if it is not the last)
            if subreport != self.subreports[-1]:
                self.insertNewPage()
                
    def generateTitle(self):
        """
         Produces the file name for the document.
  
        @return string :
        @author
        """
        if self.assessmentNumber == 2:
            if self.assessmentTimePeriod.length == 1:
                title = "cde_2aval_" + str(self.assessmentTimePeriod.year) + "s" + str(self.assessmentTimePeriod.session) + self.assessedObject.courseCode.lower()
            else:
                title = "cde_2aval_" + str(self.assessmentTimePeriod.year) + "q" + str(self.assessmentTimePeriod.session) + self.assessedObject.courseCode.lower()
        else:
            if self.assessmentTimePeriod.length == 1:
                title = "cde" + str(self.assessmentTimePeriod.year) + "s" + str(self.assessmentTimePeriod.session) + self.assessedObject.courseCode.lower()
            else:
                title = "cde" + str(self.assessmentTimePeriod.year) + "q" + str(self.assessmentTimePeriod.session) + self.assessedObject.courseCode.lower()

        return str(title)
  
    def makeSubreports(self):
        """
         Implements abstract method of superclass in order to make subreports for a
         course object.
         Create a subreport for each of the elements that must be treated individually
         inside of an assessed course (e.g. a course offer or a course class).
  
        @return  :
        @author
        """

        # gets course offers to make subreports from
        assessedOffers = Offer.find(course = self.assessedObject, timePeriod = self.assessmentTimePeriod)
        # creates a CourseSubreport for each course offer
        classesAlreadyReported = [] # list of classes that already got a subreport

        for assessedOffer in assessedOffers:
            if not OpticalSheetField.find(offer = assessedOffer):
                continue
            makeSubreport = True # boolean that indicates if the subreport should be made

            if not self.showProfessorName and self.reportByClass:
                # if the report should be made by class and should not exhibit the professors name, then we need not to repeat offers with the same class number when making subreports
                if assessedOffer.classNumber not in classesAlreadyReported:
                    classesAlreadyReported.append(assessedOffer.classNumber) # adds class number to list
                else:
                    makeSubreport = False

            if makeSubreport:   
                subreport = CourseSubreport(assessedOffer, self.templateFolder, self.reportByClass, self.assessmentNumber)
                # initializes texSource attribute for the subreport: this is necessary for it to know the reports temporary output directory (i.e. where the tex source is kept) when generating its charts
                subreport.texSource = File(self.texSource.directoryPath, self.generateTitle() + "_subreport" + str(assessedOffer.classNumber))
                # adds subreport to the subreports list attribute
                self.subreports.append(subreport)
  
    def setReportInstructions(self, faculty, assessmentNumber = 1, reportByClass = True, showProfessorName = True):
        """
         Set report specific instructions such as to count answers by class or by
         professor, or such as which assessment's answers to count.

        @param Faculty faculty : The faculty to which the course report is being presented.
        @param int assessmentNumber : Integer that indicates the number of the assessment to which the answers that must be counted were given.
        @param bool reportByClass : Boolean that marks if the course subreport should be made by class number or by professor.
        @param bool showProfessorName : Boolean that marks if the report should exhibit the names of the professors ahead of the course offers assessed.
        @return  :
        @author
        """
        # checks validity of assessmentNumber parameter
        if not isinstance(assessmentNumber, int):
            raise CourseReportError("Invalid assessmentNumber parameter: must be an integer.")
        elif assessmentNumber < 1:
            raise CourseSubreportError("Invalid assessmentNumber parameter: must be an integer greater than 1.")

        # checks validity of faculty parameter
        if not isinstance(faculty, Faculty):
            raise CourseReportError("Invalid faculty parameter: must be a Faculty object")

        # checks validity of reportByClass parameter            
        if not isinstance(reportByClass, bool):
            raise CourseReportError("Invalid reportByClass parameter: must be a boolean.")

        # checks validity of showProfessorName parameter
        if not isinstance(showProfessorName, bool):
            raise CourseReportError("Invalid showProfessorName parameter: must be a boolean.")

        self.assessmentNumber = assessmentNumber
        self.faculty = faculty
        self.reportByClass = reportByClass
        self.showProfessorName = showProfessorName
        

def hasAnswers(answerDict):
    """Returns true if the dictionary has at least 1 answer"""
    for key in answerDict:
        if answerDict[key] > 0:
            return True
    return False
