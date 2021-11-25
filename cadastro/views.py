from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
#from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django_tables2 import RequestConfig
#from django.contrib.auth.decorators import login_required
from django.db.models import Q
#from django.http import HttpResponse
from .models import Parceiro
from .forms import *
#from .forms import SearchParcForm
from .tables import Parc_table
#from util.query import qr_and_or
from .models import Municipio, Estado
from .services import *


class CadView(generic.ListView):
    paginate_by = 5 
    model = Parceiro

def lista(request):
    parc = Parc_table(Parceiro.objects.all())
    RequestConfig(request, paginate={'per_page': 10}).configure(parc)
    return render(request, 'cadastro/lista.html', {'parc': parc})

def detalhe(request, id):
    instance = Parceiro.objects.get(id=id)
    form = ParcForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        #return redirect('view_lista')
        #form = ParcForm(form.cleaned_data)
        
        return render(request, 'cadastro/parc_form.html', {'form': form})
    return render(request, 'cadastro/parc_form.html', {'form': form})

##tratamento da lista de cidades por estado
def load_cities(request):
    estado_id = request.GET.get('estado')
    municipios = Municipio.objects.filter(estado=estado_id).order_by('nome')
    print(estado_id)
    print(municipios)
    return render(request, 'cadastro/lista_cidades.html', {'municipios': municipios})
    







def importMuni(request):
    muniList = lista_munis()
    return render(request, 'cadastro/importMuni.html', {'object_list': muniList})

def pesq(request):
    return render(request, 'cadastro/pesq.html', {})

def pesquisa(request):
    form = SearchParcForm(request.POST or None)
    #form.clean()
    if form.is_valid():
        qst = Parceiro.objects.all()
        q = Q()

        if form.cleaned_data.get('nome'):
            campo = 'nome__icontains'
            pesq = form.cleaned_data.get('nome')
            q = qr_and_or(campo, pesq)
            qst = qst.filter(q)

        if form.cleaned_data.get('cnpj'):
            campo = 'cnpj__startswith'
            pesq = form.cleaned_data.get('cnpj')
            q = qr_and_or(campo, pesq)
            qst = qst.filter(q)

        if form.cleaned_data.get('cidade'):
            campo = 'municipio__nome__icontains'
            pesq = form.cleaned_data.get('cidade')
            q = qr_and_or(campo, pesq)
            qst = qst.filter(q)

        if form.cleaned_data.get('estado'):
            campo = 'estado__sigla__icontains'
            pesq = form.cleaned_data.get('estado')
            q = qr_and_or(campo, pesq)
            qst = qst.filter(q)


        #return HttpResponse(form.cleaned_data['ativo'])

        parc = Parc_table(qst)
        RequestConfig(request, paginate={'per_page': 50}).configure(parc)
        form = SearchParcForm(form.cleaned_data)
        return render(request, 'cadastro/pesq.html', {'parc': parc, 'form': form})
    else:
        return render(request, 'cadastro/pesq.html', {'form': form})


def novo(request):
    form = ParcForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('view_lista')
    return render(request, 'cadastro/parc_form.html', {'form': form})