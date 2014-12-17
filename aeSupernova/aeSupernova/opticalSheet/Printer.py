#encoding: utf8
import codecs
import commands
from django.conf import settings
from django.http.response import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from pulsarInterface.CourseCoordination import CourseCoordination
from pulsarInterface.Faculty import Faculty


class Printer(object):

    """
     A class to create a assessment PDF, it can be a Qualitative Questionnaire, an
     OpticalSheet ...

    :version:
    :author:
    """

    """ ATTRIBUTES

     The name of the file that is going to be printed.

    name  (public)

     The path where the file is going to be printed

    path  (public)

     The text to be placed in the .tex file.

    texText  (public)

    """


    def __init__(self):
        """
         Initialization method. Here the path is set using django's MEDIA_ROOT.

        @return  :
        @author
        """

        self.path = settings.MEDIA_ROOT + 'pdf/'
        self.name = None

    def loadTemplate(self, templateName, parameters):
        """
         Load the template with the given name with the given parameters to the texText
         parameter.

        @param string templateName : The name of the template to be loaded.
        @param {} parameters : The parameters to be loaded in the template.
        @return  :
        @author
        """

        t = get_template(templateName)
        self.texText = t.render(Context(parameters))

    def createPDF(self):
        """
         Create a file in this object path, and this objects name + '.tex' with the
         texText and tries to create the pdf from it, if it is successful returns True,
         if not returns False.

        @return bool :
        @author
        """

        if self.texText != None:
            tex = codecs.open(self.path + self.name + '.tex','w','utf8')
            tex.write(self.texText)
            try:
                if self.path != '':
                    commands.getoutput("pdflatex -interaction=nonstopmode -output-directory=" + self.path + " " + self.path + self.name + '.tex')               
                else:
                    commands.getoutput("pdflatex " + self.path + self.name + '.tex')               
                commands.getoutput("rm " + self.path + self.name + '.log')
                commands.getoutput("rm " + self.path + self.name + '.aux')
                return True
            except:
                return False
        else:
            return False

    def getPDF(self):
        """
         Get the pdf file created in the createPDF method, and returns it to be
         downloaded by the user of the site, also delete the .tex and .pdf files.

        @return {} :
        @author
        """


        pdf = file(self.path + self.name + '.pdf').read()
        commands.getoutput("rm " + self.path + self.name + '.tex')
        commands.getoutput("rm " + self.path + self.name + '.pdf')

        response = HttpResponse(pdf)
        response['Content-Type'] = 'application/pdf'
        response['Content-disposition'] = 'attachment; filename=' + self.name + '.pdf'
        return response 

    def getTex(self):
        """
         Get the tex file created in the createPDF method, and returns it to be
         downloaded by the user of the site, also delete the .tex and .pdf files.

        @return {} :
        @author
        """

        tex = file(self.path + self.name + '.tex').read()
        commands.getoutput("rm " + self.path + self.name + '.tex')
        commands.getoutput("rm " + self.path + self.name + '.pdf')

        response = HttpResponse(tex)
        response['Content-Type'] = 'application/tex'
        response['Content-disposition'] = 'attachment; filename=' + self.name + '.tex'
        return response 

    def createName(self, timePeriod, cycle, term):
        """
         Creates a name for the file from the parameter passed.

        @param timePeriod timePeriod : 
        @param Cycle cycle : 
        @param int term : 
        @return  :
        @author
        """

        name = str(timePeriod.idTimePeriod)
        name += "".join(letter for letter in cycle.name if ord(letter)<128).replace(' ','') #Simple way to clear non ascii letter and spaces
        name += str(term)
        self.name = name


    @staticmethod
    def createTitle(timePeriod, cycle, term):
        """
         Creates a title to be placed on top of the printed files.

        @param timePeriod timePeriod : 
        @param Cycle cycle : 
        @param int term : 
        @return  :
        @author
        """

        faculty = Faculty.find(courseCoordinations = CourseCoordination.find(cycles = [cycle]))[0]
        title = {}
        title['lines'] = []
        title['lines'].append('Consulta discente sobre o Ensino(CDE)')
        title['lines'].append(str(timePeriod) + ' da ' + faculty.name + u' de São Paulo')
        year = int(term/2) + term%2
        title['lines'].append('Representante de Classe ' + str(year) + u'º ano - ' + cycle.name) 
        return title
