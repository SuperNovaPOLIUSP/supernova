from aeSupernova.header.Header import *
from pulsarInterface.IdealTermCourse import *

def openSite(request):
    
    if request.user.is_authenticated():
        header = Header()
        header.setFacultyFunction('findCycles($("#headerFaculty").val())')
        return render_to_response('lerJupiter.html',{'header':header.getHtml()})
    else:
        return HttpResponseRedirect('/login/')

def lerJupiter(request):
    data = request.GET
    idCycles = json.loads(data['idCycles']) #Do something with this list
    idCycles = [int(idCycle) for idCycle in idCycles]
    idTimePeriod = int(data['idTimePeriod'])
    print idCycles
    print idTimePeriod
    return HttpResponse('ok')
