from django.contrib.auth.decorators import login_required
from pulsarInterface.IdealTermCourse import *
from aeSupernova.header.Header import *


@login_required
def openSite(request):
    header = Header()
    header.setFacultyFunction('findCycles($("#headerFaculty").val())')
    return render_to_response('lerJupiter.html',{'header':header.getHtml()})

def lerJupiter(request):
    data = request.GET
    idCycles = json.loads(data['idCycles']) #Do something with this list
    idCycles = [int(idCycle) for idCycle in idCycles]
    idTimePeriod = int(data['idTimePeriod'])
    print idCycles
    print idTimePeriod
    return HttpResponse('ok')
