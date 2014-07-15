#Embedded file name: /home/www/aeSupernova/aeSupernova/presentation/Presentation.py
from django.template.loader import *
from django.http import *
import apresentacao2

class Presentation(object):

    @staticmethod
    def findReports(idTimePeriod, idFaculty, idCycle, term):
        reports = apresentacao2.findReports(idTimePeriod, idFaculty, idCycle, term)
        return reports

    @staticmethod
    def getReport(data):
        path = settings.MEDIA_ROOT + 'relatorios/disciplinas/'
        folder = str(data['course']['id']) + '/'
        reportName = 'cde' + str(data['year']['name']) + 's' + str(data['session']['name']) + str(data['course']['name']).lower() + '.pdf'
        pdf = file(path + folder + reportName).read()
        response = HttpResponse(pdf)
        response['Content-Type'] = 'application/pdf'
        response['Content-disposition'] = 'attachment; filename=' + reportName
        return response
