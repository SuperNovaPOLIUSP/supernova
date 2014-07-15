from aeSupernova.opticalSheet.Printer import *
from pulsarInterface.OpticalSheet import *
from pulsarInterface.Faculty import *

#import operator

class QualitativeQuestionnairePrinter(Printer):

    """
     A class to create the qualitative questionnaire's PDF from an OpticalSheet.

    :version:
    :author:
    """

    """ ATTRIBUTES

     The cycle of this QualitativeQuestionnaire.

    cycle  (public)

     The timePeriod of this QualitativeQuestionnaire.

    timePeriod  (public)

     The term of this QualitativeQuestionnaire.

    term  (public)

     This qualitativeQuestionnaire's opticalSheet.

    opticalSheet  (public)

     The title on top of this QualitativeQuestionnaire's first page.

    title  (public)

     If it is true the questions must not have the course's name writen.

    noCourseName  (public)

     A bool showing if the related opticalSheet is encoded.

    encoded  (public)

     A dict with the keys:
     font : the font size to be used for the courses in the second page
     courses: a list of course's name and the description of each offer related.
     

    courses  (public)

    """

    def __init__(self, idTimePeriod, idCycle, term):
        """
         Initialization method.

        @param int idTimPeriod : The database id of the timePeriod if this QualitativeQuestionnaire.
        @param int idCycle : The database id of the cycle if this QualitativeQuestionnaire.
        @param int term : The term this QualitativeQuestionnaire.
        @return  :
        @author
        """

        Printer.__init__(self)
        self.cycle = Cycle.pickById(idCycle)
        self.timePeriod = TimePeriod.pickById(idTimePeriod)
        self.term = term
        self.createName()

    def printQualitativeQuestionnaire(self, idOpticalSheet, numberOfAnswerLines, qualitativeQuestionnaireType):
        """
         Set all of this objects paramters and use the function loadTemplate with its
         __dict__ and the template 'qualitativeQuestionnaireTemplate.tex'

        @param int idOpticalSheet : The id of the opticalSheet of related to this QualitativeQuestionnaire.
        @param int numberOfLines : The number of lines in each question of this QualitativeQuestionnaire.
        @param int qualitativeQuestionnaireType : The type of the QualitativeQuestionnaire:
            if it is 1: The name of each course should be shown in the questions.
            if it is 2: The questions must have a line for the student to write the course's name.
        @return  :
        @author
        """

        self.opticalSheet = OpticalSheet.pickById(idOpticalSheet)
        self.opticalSheet.fillOpticalSheetFields()
        self.title = Printer.createTitle(self.timePeriod, self.cycle, self.term)
        if qualitativeQuestionnaireType == 1:
            self.noCoursesName = True
        if self.opticalSheet.encodingName != None:
            self.encoded = True
            self.courses = QualitativeQuestionnairePrinter.createCodes(self.opticalSheet.fields)
        else:
            self.courses = QualitativeQuestionnairePrinter.createCourses(self.opticalSheet.fields)
        self.numberOfAnswerLines = range(numberOfAnswerLines) #This is the only way django template understands   

        self.loadTemplate('texTemplates/qualitativeQuestionnaireTemplate.tex', self.__dict__)
        self.createPDF()
   
    def createName(self):
        """
         Call the createName method of the Printer class, and appends a 'QQ' in the start
         of the name.

        @return  :
        @author
        """

        Printer.createName(self, self.timePeriod, self.cycle, self.term)
        self.name = 'QQ' + self.name.replace('/', '_')  # Bugfix: Names with '/' do not go well in an Unix environment

    @staticmethod
    def createCodes(fields): 
        """
         Create the courses parameter if the opticalSheet related to this
         qualitativeQuestionnaire is encoded.

        @param OpticalSheetFields[] fields : A list of OpticalSheetFields objects, of an opticalSheet.
        @return  :
        @author
        """

        #First group them by course
        courses = {}
        for field in fields:
            if not field.offer.course.idCourse in courses.keys():
                courses[field.offer.course.idCourse] = []
            courses[field.offer.course.idCourse].append(field)
        #Now prepare the list to be used in django's template
        sets = []
        for idCourse in courses:
            courseDict = {}
            courseDict['courseName'] = courses[idCourse][0].offer.course.name
            courseDict['offers'] = []
            for field in courses[idCourse]:
                codeDict = {}
                codeDict['classNumber'] = str(field.offer.classNumber)
                codeDict['professor'] = field.offer.professor.name
                codeDict['schedule'] = '/'.join([str(schedule).split(' - ')[0] for schedule in field.offer.schedules]) #Get part of the schedule string
                if int(field.code) < 99:
                    codeDict['code'] = str(field.code).zfill(2)
                else:
                    #raise OpticalSheetError("It's over one hundred!")
                    codeDict['code'] = str(field.code).zfill(2)
                courseDict['offers'].append(codeDict)
            #courseDict['offers'].sort(key=operator.attrgetter('code'))
            sets.append(courseDict)
        courses['courses'] = sets
        return courses

    @staticmethod
    def createCourses(fields): 
        """
         Create the courses parameter if the opticalSheet related to this
         qualitativeQuestionnaire is not encoded.

        @param OpticalSheetFields[] fields : A list of OpticalSheetFields objects, of an opticalSheet.
        @return  :
        @author
        """

        courses = {}
        courses['courses'] = []
        offersSet = {} 
        #First try to group them by courseIndex.
        for field in fields:
            if not field.courseIndex in offersSet.keys():
                offersSet[field.courseIndex] = []
            offersSet[field.courseIndex].append(field.offer)
        #Now create the necessari dict for the template
        for courseIndex in offersSet:
            course = {}
            course['name'] = offersSet[courseIndex][0].course.name + Offer.offersName([offersSet[courseIndex]])[0] #Get the courses name from any of the offers
            course['offers'] = []
            for offer in offersSet[courseIndex]:
                offerDict = {}
                if not offer.classNumber in [sameOffer['classNumber'] for sameOffer in course['offers']]: #Offers of the same classNumber should be showed together
                    offerDict['classNumber'] = offer.classNumber
                    offerDict['schedule'] = '/'.join([str(schedule).split(' - ')[0] for schedule in offer.schedules]) #Get part of the schedule string
                    offerDict['professor'] = offer.professor.name
                    course['offers'].append(offerDict)
                else:
                    [sameOffer for sameOffer in course['offers'] if sameOffer['classNumber'] == offer.classNumber][0]['professor'] = '' #If offers are showed together no professor's name should appear

            #Now organize the offers in columns 
            if len(course['offers']) > 8: #if there are more than 10 offers to show split them in 2 columns.
                columns = []
                i = 0
                i2 = 0
                for offer in course['offers']:
                    if i <= int(len(course['offers'])/2):
                        columns.append([offer])
                        i = i + 1
                    else:
                        columns[i2].append(offer)
                        i2 = i2 + 1
                while(i2 < i): #In this case you have to complete with empty spaces
                    columns[i2].append(None)
                    i2 += 1
                course['offers'] = columns
            else:
                course['offers'] = [ [offer] for offer in course['offers']] #Only one column.
            courses['courses'].append(course)

        #Now count the number of lines to define the font size to be used
        numberOfLines = 0
        for course in courses['courses']:
            numberOfLines += len(course['offers'])
        if numberOfLines > 50:
            courses['font'] = 6
        else:
            courses['font'] = 8 

        return courses

