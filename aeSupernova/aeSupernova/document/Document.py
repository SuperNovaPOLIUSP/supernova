from File import *
from aeSupernova.header.Header import *

from django.template import Template, Context  # package for the use of templates
import os                                      # package for basic OS operations
import commands                                # package for the use of command line instructions
import codecs                                  # package to manipulate unicode files
import subprocess
import shlex
from django.conf import settings

class DocumentError(Exception):
    """
     Exception reporting an error in the execution of a Document operation.

    :version:
    :author:
    """
    pass

class Document (object):
  
    """
     Class that models a LaTeX document, providing operations to create, add content
     to and produce a pdf document through a LaTeX.
  
    :version:
    :author:
    """
  
    """ ATTRIBUTES
  
     String containing the LaTeX source code for the document.
  
    contents  (public)
  
     PDF file that contains the final version of the document produced through the
     compilation of the LaTeX source code.
  
    finalDocument  (public)
  
     Absolute path to the directory where are stored the templates to be used to
     generate content for the document.
  
    templateFolder  (public)
  
     Tex file which contains the source code for the document.
  
    texSource  (public)
  
    """
  
    def __init__(self, templateFolder):
        """
         Constructor method.
  
        @param string templateFolder : Absolute path to the directory where are stored the templates to be used to generate content for the document.
        @return  :
        @author
        """
        
        # verifies validity of templateFolder parameter
        if not isinstance(templateFolder, str):
            raise DocumentError("Invalid templateFolder parameter: must be a string.")
        elif not os.path.exists(templateFolder):
            raise DocumentError("Invalid templateFolder parameter: directory does not exist.")
        else:
            # tries to access the directory
            try:
                os.chdir(templateFolder)
            except:
                raise FileError("Invalid templateFolder parameter: access denied.")
  
        # attribute initialization
        self.templateFolder = templateFolder
        self.contents = ""
        self.finalDocument = None
        self.texSource = None
  
    def generateContents(self):
        """
         Generates a string with the contents of the LaTeX source code that will be
         compiled in order to produce the document. Must be overwritten by child classes
         in order to generate the documents specific contents.
  
        @return  :
        @author
        """
        # abstract method
        pass
  
    def generateTitle(self):
        """
         Produces the file name for the document.
  
        @return  :
        @author
        """
        # abstract method
        pass
  
    def insertNewPage(self):
        """
         Inserts new page in the documents contents.
  
        @return  :
        @author
        """
        self.contents += "\n\\newpage\n"
  
    def renderFromTemplate(self, templateFileName, templateParameters):
        """
         Concatenates, with the document contents, a string generated through the
         renderization of a specified template with the specified list of parameters.
  
        @param string templateFileName : Name of the template used to generate part of the documents contents.
        @param {} templateParameters : Dictionary of parameters to be used by the template in order to generate contents for the document.
        @return  :
        @author
        """
  
        # verifies if the parameters are valid
        if not isinstance(templateFileName, str):
            raise DocumentError("Invalid templateFileName parameter: must be a string")
        if not isinstance(templateParameters, dict):
            raise DocumentError("Invalid templateParameters parameter: must be a dictionary.")
  
        # opens template
        #try:
        templateModel = Template(codecs.open(os.path.join(self.templateFolder, templateFileName), 'r', 'utf-8').read())
        #except:
        #    raise DocumentError("Template error: could not open template.")
  
        # renders template
        try:
            self.contents += templateModel.render(Context(templateParameters))
        except:
            raise DocumentError("Template error: could not render template.")
  
    def writeDocument(self, outputDirectory):
        """
         Writes the current source code (with proper finalization) of the document in a
         .tex file created in a temporary directory. Then compiles it using pdflatex and
         moves the resulting pdf file to the specified output directory.
  
        @param string outputDirectory : Absolute path to the directory to where the document must be moved after being produced.
        @return  :
        @author
        """
  
        # tries to create File objects to manipulate the source and the final documents
        try:
            self.finalDocument = File(outputDirectory, self.generateTitle() + '.pdf') # final document
            self.texSource = File(os.path.join(outputDirectory, "temp_" + self.generateTitle()), self.generateTitle() + '.tex') # source code
        except:
            raise DocumentError("Failed to access output directory.")
  
        # produces the documents contents
        self.generateContents()
        try:
            self.contents += u"\n\\end{document}\n\n" # finishes LaTeX document
        except:
            raise DocumentError("Failed while generating documents contents.")
  
        # opens a file to contain the LaTeX source code
        self.texSource.workWithFile()
        self.texSource.realFile = codecs.open(self.texSource.fileName, 'w', 'utf-8')
  
        # writes the content generated to source file
        self.texSource.realFile.write(self.contents)
  
        self.texSource.workWithFile() # changes directory
  
        # compiles the source into a pdf document
        #try:
            #compilationCommand = 'pdflatex -interaction=nonstopmode --output-directory=' + outputDirectory + ' ' + self.texSource.fileName
            #output = commands.getoutput(compilationCommand)
        abspath = outputDirectory + '/' + 'temp_' + self.texSource.fileName[0:-4] + '/' + self.texSource.fileName
        proc = subprocess.Popen(shlex.split('pdflatex -interaction=nonstopmode --output-directory=' + outputDirectory + ' ' + abspath))
        proc.communicate()
        #try:
        #    abspath = outputDirectory + '/' + 'temp_' + self.texSource.fileName[0:-4] + '/' + self.texSource.fileName
        #    check_output(["pdftex", "-interaction=nonstopmode --output-directory=" + outputDirectory + ' ' + abspath], shell = True)
        #except CalledProcessError as e:
        #    return e.output
        #except:
        #    print b
        #    raise DocumentError("Failed to compile LaTeX source code.")
        
        # erases source files
        self.texSource.deleteFile(True)
        self.finalDocument.workWithFile()
        os.remove(self.generateTitle() + ".aux")
        os.remove(self.generateTitle() + ".log")
        os.chdir(settings.PASTA_SUPERNOVA)
