from pulsarInterface.Offer import *
from pulsarInterface.OpticalSheet import *
from pulsarInterface.Answer import *
from pulsarInterface.Datafile import *

##data we got:
#datafileName
#idCycle
#term
#idTimePeriod
#bSheet #zero for A or one for B
#faculty
#assessmentNumber

class NoteReader(object):
    @staticmethod
    def readNote(datafileName, datafileFile, idCycle, term, idTimePeriod, bSheet, assessmentNumber):
        f = datafileFile.split('\n')

        #reading the .dat
        #lines into list
        dat = []
        for line in f:
            try:
                split_line = line.split('N ')[1]
                dat.append(split_line)
            except:
                pass
        cycles = [Cycle.pickById(idCycle)]
        try:
            opticalSheet = OpticalSheet.find(term = term, cycles = cycles, timePeriod = TimePeriod.pickById(idTimePeriod))[0]
        except:
            raise OpticalSheetError('Optical Sheet not found')
        #splitting the lines by collumn
        data = []
        for os in dat: #os stands for optical sheet
            os = os[:-1]
            os_list = []
            for r in range(0, len(os), 12):
                os_list.append(os[r:r+12])
            data.append(os_list)

        #let's create answertypes
        answers = []
        identifier = 0
        for os in data:
            identifier += 1
            courseIndex = 10*bSheet
            for collumn in os:
                courseIndex += 1
                try:
                    code = int(collumn[:2])
                    for questionIndex in range(10):
                        answer = Answer(questionIndex+1, collumn[questionIndex+2], identifier)
                        answer.setCourseIndex(courseIndex)
                        answer.setCode(code)
                        answers.append(answer)
                except: 
                    pass
        datafile = Datafile(datafileName)
        datafile.setAnswers(answers)
        badAnswers = opticalSheet.storeDatafile(datafile,assessmentNumber)
        #badAnswers = [] #teste
        goodAnswers = [answer for answer in answers if answer not in badAnswers]
        #function returns a list of dictionaries, one for each bad answer, with bad answers' 'code', 'courseIndex' and 'identifier' as keys. 
        badAnswers_datum = []
        for badAnswer in badAnswers:
            badAnswer_data = {}
            badAnswer_data['code'] = badAnswer.code
            badAnswer_data['courseIndex'] = badAnswer.courseIndex
            badAnswer_data['identifier'] = badAnswer.identifier
            badAnswers_datum.append(badAnswer_data)
        goodAnswers_datum = []
        for goodAnswer in goodAnswers:
            goodAnswers_data = {}
            goodAnswers_data['code'] = goodAnswer.code
            goodAnswers_data['courseIndex'] = goodAnswer.courseIndex
            goodAnswers_data['identifier'] = goodAnswer.identifier
            goodAnswers_datum.append(goodAnswers_data)
        return {'good':goodAnswers_datum, 'bad':badAnswers_datum}
