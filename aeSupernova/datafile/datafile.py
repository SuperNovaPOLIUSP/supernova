from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from NoteReader import *
from aeSupernova.header.Header import *


def translateAnswerListOfDict(answersList):
    stringList = []
    for answerDict in answersList:
        stringList.append('Answer: code ' +str(answerDict['code']) +', courseIndex ' +str(answerDict['courseIndex']) +', identifier ' +str(answerDict['identifier']))
    return stringList

@login_required
def openSite(request):
    header = Header()
    header.setTermFunction('$("#file").show()')
    if request.method == 'POST':
        data = request.POST
        answers = NoteReader.readNote(request.FILES['arq'].name, request.FILES['arq'].file.getvalue(),int(data['headerCycle']), int(data['headerTerm']), int(data['headerTimePeriod']), int(data['bSheet']), int(data['assessmentNumber']))
    return render_to_response('datafile.html',{'divs':header.getHtml()},context_instance=RequestContext(request))
    
def read(request):
    data = request.GET
    #NoteReader.readNote(datafileFile, idCycle, term, idTimePeriod, bSheet, assessmentNumber)
    NoteReader.readNote(data['datafileFile'],data['idCycle'],data['term'],data['idTimePeriod'],data['bSheet'],data['assessmentNumber'])

def dict2string(dict):
    texto = ''
    for key in dict:
        texto += ' {"'+str(key)+'":'+str(dict[key]) +'}\n'
    return texto
