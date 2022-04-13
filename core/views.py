from django.shortcuts import render
from core.rpt_linha_pdf import *
import core.label_pdf as lbl
from django.http.response import HttpResponse

def index(request):
    return render (request, 'index.html')



'''

def label_pdf(request):

    lbl_width = 100
    lbl_height = 80
    emissor = 'DEFER INDUSTRIA METALURGICA'
    destinatario = 'HERVAL MÓVEIS'
    nf = '1223455'
    volumes = 20

    vol = []
    for i in range(1, volumes + 1):
        vol.append(str(i))
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Relatorio.pdf"'
    buffer = BytesIO()
    
    meuKwarg = {}
    meuKwarg['width'] = lbl_width
    meuKwarg['height'] = lbl_height
    meuKwarg['destinatario'] = destinatario
    meuKwarg['nf'] = nf
    meuKwarg['volumes'] = vol
    meuKwarg['emissor'] = emissor

    rep = lbl.Label_volumes(buffer, **meuKwarg)
    #pdf = rep.generateReport()
    response.write(rep.show())
    return response


    '''