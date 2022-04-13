from .forms import Label_form
from django.shortcuts import render
from django.http.response import HttpResponse
#from .reports import *
from io import BytesIO
from .reports import Label_volumes


# Create your views here.
def label(request):

    if request.method == 'POST':
        emi = request.POST.get('emitente') if request.POST.get('emitente') else ''
        dest = request.POST.get('destinatario') if request.POST.get('destinatario') else ''
        nf = request.POST.get('nf') if request.POST.get('nf') else ''
        volumes = request.POST.get('volumes') if request.POST.get('volumes') else ''
        num_ped = request.POST.get('num_ped') if request.POST.get('num_ped') else ''
        num_oc = request.POST.get('num_oc') if request.POST.get('num_oc') else ''

        lbl_width = 100
        lbl_height = 50
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="Relatorio.pdf"'
        buffer = BytesIO()
        
        print('flag 1')
        meuKwarg = {}
        meuKwarg['width'] = lbl_width
        meuKwarg['height'] = lbl_height
        meuKwarg['destinatario'] = dest
        meuKwarg['nf'] = nf
        meuKwarg['num_ped'] = num_ped
        meuKwarg['num_oc'] = num_oc
        meuKwarg['volumes'] = int(volumes)
        meuKwarg['emissor'] = emi
        print('flag 2')

        rep = Label_volumes(buffer, **meuKwarg)
        #pdf = rep.generateReport()
        response.write(rep.show())
        return response

    frlbl = Label_form()
    print(request)
    return render(request, 'reports/label.html', {'form' : frlbl})

