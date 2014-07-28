# coding: utf8
"Object that will read all cycles of a Faculty"
import MySQLdb
from Crawler.Crawler import Crawler
from Crawler.Crawler import appendparameters
from pulsarInterface.Faculty import Faculty


class FacultyReader(object):
    """A reader object which will use a crawler to scan through the cycles
    of a faculty"""
    def __init__(self):
        self.connection = None
        self.timeperiod = None
        self.faculty = None
        self.crawler = Crawler()

    @staticmethod
    def initwithconnection(host, user, password, database):
        """Returns a new CycleReader object with its connection already
        configured using the host, user, password and database name
        provided as parameters. Additionally, it configures the charset
        to be used as unicode"""
        facultyreader = FacultyReader()
        facultyreader.connection = MySQLdb.connect(host=host, user=user,
                                                   passwd=password,
                                                   db=database,
                                                   use_unicode=True,
                                                   charset='utf8')
        return facultyreader

    def settimeperiod(self, idtimeperiod):
        "Sets the timeperiod of this cycle by providing its id"
        self.timeperiod = idtimeperiod

    def setfaculty(self, idfaculty):
        "Sets the cycle of this reader by searching for the cycle in the bank"
        self.faculty = Faculty.pickById(idfaculty)

    def startreading(self):
        """Starts scanning through the Faculty's page and iterates through each
        of it's cycles"""
        urlstart = 'https://uspdigital.usp.br/jupiterweb/jupCursoLista'
        parameters = {'codcg': self.faculty.idFaculty, 'tipo': 'N'}
        completeurl = appendparameters(urlstart, parameters)
        self.crawler.loadpage(completeurl)
