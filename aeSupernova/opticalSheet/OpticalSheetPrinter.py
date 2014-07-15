#encoding: utf8
from aeSupernova.opticalSheet.Printer import *
from pulsarInterface.OpticalSheet import *
from pulsarInterface.Faculty import *

class OpticalSheetPrinter(Printer):
    """
     A class to create the opticalSheet's PDF.

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

     The faculty related to this opticalSheet.

    faculty  (public)

     If there is a picture to be placed set the path to it.

    picture  (public)

     A dict with the keys:
     > positions: [float, float]
     > tabular: a string representing the structure of the table in LaTeX
     > lines: a list of dicts where each list is a line in the table and each dict is
     a cell with the keys: font and text.

    table  (public)

     A list of lists of dicts where each list represent a set of 10 or less dicts
     that represent a course in the opticalSheet and heva the keys: font: int,
     position: [float, float], abbreviation: string.
     
     Each new inner list represents another page in the opticalSheet.

    coursesList  (public)

     A ist of dicts, where each dict represents a question in the opticalSheet, with
     the keys: position:[float, float], font and questionWording.

    questions  (public)

    """


    def __init__(self,idCycle, term, idTimePeriod):
        """
         Initialization method.

        @param int idTimPeriod : The database id of the timePeriod if this QualitativeQuestionnaire.
        @param int idCycle : The database id of the cycle if this QualitativeQuestionnaire.
        @param int term : The term this QualitativeQuestionnaire.
        @return  :
        @author
        """

        Printer.__init__(self)
        self.timePeriod = TimePeriod.pickById(idTimePeriod)
        self.cycle = Cycle.pickById(idCycle)
        self.term = term
        self.createName()
        
    def printOpticalSheet(self, idOpticalSheet, fields, survey, positions):
        """
         Set all of this objects paramters and use the function loadTemplate with its
         __dict__ and the template 'opticalSheetTemplate.tex'

        @param int idOpticalSheet : The id of the opticalSheet of related to this QualitativeQuestionnaire.
        @param [] fields : A list of dicts representing the courses in an OpticalSheet.  the dicts have the keys: abbreviation, font, courseIndex.
        @param {} survey : Survey is a dict with the keys:

            > instructions: a list of dicts with idAnswerType and font, that represent the chosen answerTypes to show in the opticalSheet.

            > questions: a list of dict with questionWording, font and idAnswerTypes

        @param {} positions : A dict with the keys:
            tableX: position X of the table
            tableY: position Y of the table
            ColumnX:position X of the 1ºcolumn
            ColumnY: position Y of the 1º column
            ColumnDX: horizontal distance between the columns
            QuestionX: position X of the 1º question
            QuestionY: position Y of the 1º question
            QuestionDY: vertical distances between the questions.
        @return  :
        @author
        """

        self.opticalSheet = OpticalSheet.pickById(idOpticalSheet)
        self.faculty = Faculty.find(courseCoordinations = CourseCoordination.find(cycles = [self.cycle]))[0]
        if self.faculty.name == u'Escola Politécnica':
            self.picture = '{' + settings.MEDIA_ROOT + 'images/minerva.png}' #The {} have to be here because django's template think they are commands
        self.title = OpticalSheetPrinter.createTitle(self.timePeriod, self.cycle, self.term) 
        self.table = OpticalSheetPrinter.organizeInstructions(survey['instructions'], survey['questions'], float(positions['tableX']), float(positions['tableY']))
        if self.opticalSheet.encodingName == None:
            self.coursesList = OpticalSheetPrinter.createCourses(fields, float(positions['columnsX']), float(positions['columnsY']), float(positions['columnsDX']))
        else:
            self.coursesList = OpticalSheetPrinter.createEncodedCodes(float(positions['columnsX']), float(positions['columnsY']), float(positions['columnsDX']))
        self.questions = OpticalSheetPrinter.createQuestions(survey['questions'], float(positions['questionnaireX']), float(positions['questionnaireY']), float(positions['questionnaireDY']))

        self.loadTemplate('texTemplates/opticalSheetTemplate.tex', self.__dict__)
        print self.createPDF()

    def createName(self):
        """
         Call the createName method of the Printer class, and appends a 'OS' in the start
         of the name.

        @return  :
        @author
        """

        Printer.createName(self, self.timePeriod, self.cycle, self.term)
        self.name = 'OS' + self.name.replace('/', '_')  # Bugfix: Names with '/' do not go well in an Unix environment

    @staticmethod
    def createEncodedCodes(positionX, positionY, dX):
        """
         Create the coursesList parameter if the opticalSheet is encoded, in this case
         all course's name are 'code' and all fonts are 9.

        @param float positionX : 
        @param float positionY : 
        @param float dX : 
        @return  :
        @author
        """

        courses = []
        for i in range(10):
            course = {}
            course['abbreviation'] = u'código' 
            course['font'] = 9
            course['position'] = [positionX, positionY]
            positionX += dX
            courses.append(course)
        return [courses] #Returns a list to fit with the nonEncoded

    @staticmethod
    def createCourses(fields, positionX, positionY, dX):
        """
         Create the coursesList parameter if this opticalSheet is not encoded

        @param OpticalSheetFields[] fields : A list of OpticalSheetFields objects, of an opticalSheet.
        @param float positionX : The position X of the 1º column.
        @param float positionY : The position Y of the first column.
        @param float dX : The horizontal distance between 2 columns.
        @return  :
        @author
        """

        coursesA = []
        coursesB = []
        for field in fields:
            if field['courseIndex'] == 10:
                positionX = 9
            if field['abbreviation'] != '':
                course = {}
                course['abbreviation'] = field['abbreviation']
                course['font'] = field['font']
                course['position'] = [positionX, positionY]
                positionX += dX
                if field['courseIndex'] < 10:
                    coursesA.append(course)
                else:
                    coursesB.append(course)
        coursesList = []
        coursesList.append(coursesA)
        if len(coursesB) > 0:
            coursesList.append(coursesB)
        return coursesList


    @staticmethod
    def createQuestions(questions, positionX, positionY, dY):
        """
         Create the questions parameter of this object.

        @param [] questions : A list of dicts with the keys: questionWording and font.
        @param float positionX : The position X of the 1º question.
        @param float positionY : The position Y of the 1 question.
        @param float dY : The vertical distance between the questions.
        @return  :
        @author
        """

        questionsList = []
        for question in questions:
            if isinstance(question['questionWording'],(str, unicode)):
                questionDict = {}
                questionDict['questionWording'] = str(1+questions.index(question)) +' - '+ question['questionWording']
                questionDict['font'] = question['font']
                questionDict['position'] = [positionX, positionY]
                positionY += dY
                questionsList.append(questionDict)
        return questionsList


    @staticmethod
    def organizeInstructions(instructions,questions, positionX, positionY):
        """
         Creates the instructions table based on the instructions chosen by the user, and
         the question in with they appear.

        @param [] instructions : A list of dicts with idAnswerType and font, that represent the chosen answerTypes to show in the opticalSheet.
        @param [] questions : A list of dicts with the keys: questionWording and font.
        @param float positionX : The position X of the instructions table.
        @param float positionY : The position Y of the instructions table.
        @return  :
        @author
        """

        table = {}
        tabular = '|c|'
        tableLines = [[{'text':'', 'font':9}],[{'text':'A', 'font': 9}],[{'text':'B', 'font':9}],[{'text':'C','font':9}],[{'text':'D', 'font':9}],[{'text':'E', 'font':9}]]
        tablePosition = [positionX, positionY]
        for instruction in instructions:
            if int(instruction['idAnswerType']) != 0:
                #Find out which questions use it
                column0 = ''
                questionIndexList = []
                for question in questions:
                    if question['idAnswerType']!= None and int(question['idAnswerType']) == int(instruction['idAnswerType']):
                        questionIndexList.append(question['questionIndex'] + 1)
                i = 0
                for questionIndex in questionIndexList:
                    if i == 0:
                        column0 += str(questionIndex)
                    elif i == (len(questionIndexList) - 1):
                        if (questionIndexList[i-1] + 1) == questionIndex:#the end of a sequal than put 'a'
                            column0 +=' a ' + str(questionIndex)
                        else:
                            column0 += ', ' + str(questionIndex)
                    else:
                        if (questionIndexList[i-1] + 1) == questionIndex: #if it is a sequence only put the last number
                            if (questionIndex + 1) != questionIndexList[i+1]: #The next number is not in a sequence
                                column0 += ' a ' + str(questionIndex)
                        else:
                            column0 += ', ' + str(questionIndex)
                    i += 1
                tableLines[0].append({'text':column0, 'font':9})
                tabular = tabular + 'c|'
                answerType = AnswerType.pickById(int(instruction['idAnswerType']))
                i = 1
                #Now write the meanings in the table
                #for meaning in answerType.alternativeMeaning:
                for chr_index in range(65,65+len(answerType.alternativeMeaning)):
                    tableLines[i].append({'text': answerType.alternativeMeaning[chr(chr_index)], 'font':instruction['fonts'][i-1]})
                    i += 1
#        for line in tableLines:
#            line = line + '\\ \hline'
        table['lines'] = tableLines
        table['tabular'] = tabular
        table['positions'] = tablePosition
        return table

