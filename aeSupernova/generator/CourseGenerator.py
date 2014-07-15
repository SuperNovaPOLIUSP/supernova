from aeSupernova.document.CourseReport import *
from pulsarInterface.TimePeriod import *
from pulsarInterface.Faculty import *
from pulsarInterface.Course import *
import subprocess
from subprocess import CalledProcessError
#from aeSupernova.generator.CourseiReportGenerator import *
#from aeSupernova.generator.CourseReportGenerator import *

class CourseReportGenerator(object):
    def __init__(self, idTimePeriod,
        idCourses,
        useProfessorsName,
        byOffer,
        idFaculty,
        assessmentNumber):

        outputDirectory = "/home/www/public/relatorios/disciplinas"

        timePeriod = TimePeriod.pickById(idTimePeriod)
        faculty = Faculty.pickById(idFaculty)

        for idCourse in idCourses:
            course = Course.pickById(idCourse)
            
            courseReport = CourseReport(course, timePeriod, "/home/www/aeSupernova/aeSupernova/document/templates")
            courseReport.setReportInstructions(faculty, assessmentNumber, not byOffer, useProfessorsName)
            courseReport.writeDocument(outputDirectory + "/" + str(idCourse))
            timePeriodStr = str(timePeriod.year)
            if timePeriod.length == 1:
                timePeriodStr += "s"
            elif timePeriod.length == 2:
                timePeriodStr += "q"
            else: raise TimePeriodError("Invalid timePeriod length")
            timePeriodStr += str(timePeriod.session)
            try:
                subprocess.check_call(['cp', outputDirectory + '/' + str(idCourse) + '/' + courseReport.generateTitle() + ".pdf", "/home/www/public/relatorios/separado_por_semestres/" + timePeriodStr + '/'])  # Copia o relatorio para a pasta com os relatorios separados por semestres... por algum motivo
            except CalledProcessError:
                print 'Relatorio nao foi copiado para a disciplina ' + unicode(course)
            #courseReport.writeDocument(outputDirectory[:-11] + "separado_por_semestres/" + timePeriodStr)
