#encoding: utf8
import commands
from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
 
def initAlgeLin(request):
    return render_to_response('algeLin.html',{},context_instance=RequestContext(request))

def imagemAlgeLin(request):
    image_data = open("/home/www/aeSupernova/aeSupernova/algeLin/posicao.jpg", "rb").read()
    return HttpResponse(image_data, mimetype="image/png")

def algeLin(request):
    dados = request.POST
    circulos = open('/home/www/public/algeLin/circulos.tex','w')
    circulos.write('''
    \documentclass[a4paper]{article}
    \usepackage{amsmath, amssymb, amsthm, times, fullpage, float, anysize}
    \usepackage[utf8]{inputenc}
    \marginsize{0cm}{0cm}{0cm}{0cm}
    \\begin{document}
    \pagenumbering{gobble}
    \setlength{\unitlength}{0.1mm}
    ''')
    dy = int(dados['dy'])
    dx = int(dados['dx'])
    x0 = int(dados['x0'])
    y0 = int(dados['y0'])
    w = int(dados['w'])/10
    h = int(dados['h'])
    copias = int(dados['copias'])
    alturaLinha = int(dados['alturaLinha'])
    alturaTexto = int(dados['alturaTexto'])
    margemTexto = int(dados['margemTexto'])
    text = dados['text'].encode("utf-8")
    for i in range(100):
        for n in range(copias):
            y1 = y0 - (i%10)*dy
            y2 = y0 - (i/10)*dy
            x1 = x0 + dx 
            x2 = x0
            circulos.write('''
            \\begin{picture}(2970, 2850)(0, 0)
            \put('''+str(margemTexto)+''','''+str(alturaTexto)+'''){\makebox(10,10)[s]{\Huge '''+text+'''}}
            \put(50,'''+str(alturaTexto-150)+'''){\makebox(10,10)[s]{\large Numero USP:\\underline{\hspace{5cm}}  Turma:\\underline{\hspace{2cm}}}}
            \linethickness{3000mm}
            \put(0,'''+str(alturaLinha)+'''){\line(0,0){3}}
            \linethickness{'''+str(w)+'''mm}
            \put('''+str(x1)+''', '''+str(y1)+'''){\line(0,0){'''+str(h)+'''}}
            \put('''+str(x2)+''', '''+str(y2)+'''){\line(0,0){'''+str(h)+'''}}
            \end{picture}
            \\newpage
            ''')
    circulos.write('''
    \end{document}
    
    ''')
    
    circulos.close()
    #commands.getoutput('pdflatex /home/www/public/algeLin/circulos.tex')
    #commands.getoutput('mv circulos* /home/www/public/algeLin/')
    commands.getoutput('pdflatex -output-directory /home/www/public/algeLin/media /home/www/public/algeLin/circulos.tex')
    return HttpResponse('ok')

def abrirFolha(request):
    filename = '/home/www/public/algeLin/media/circulos'
    response = HttpResponse(file(filename + '.pdf').read())
    response['Content-Type'] = 'application/pdf'
    response['Content-disposition'] = 'attachment; filename= circulos.pdf'
    commands.getoutput("rm "+filename+".pdf")
    commands.getoutput("rm "+filename+".log")
    commands.getoutput("rm "+filename+".aux")
    commands.getoutput("rm /home/www/public/algeLin/circulos.tex")
    return response
        
