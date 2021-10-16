from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django_tables2 import SingleTableView
from django_tables2   import RequestConfig
from .models import Prod, Produto, Grupo, Unid, NCM
from .tables import *
from .forms import *
from .filters import *
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction
from django.forms import modelformset_factory, inlineformset_factory

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


def prodcomp(request, produto_id):
    produto = Prod.objects.get(pk=produto_id)
    #componentesFormSet = modelformset_factory(ProdComp, fields=('codComp', 'qtd',))
    componentesFormSet = inlineformset_factory(Prod, ProdComp, fk_name='codProd', fields=['codComp', 'qtd',]) 
    
    if request.method == 'POST':
        #formset = componentesFormSet(request.POST, queryset=ProdComp.objects.filter(codProd=produto.id))
        formset = componentesFormSet(request.POST, instance=produto)
        if formset.is_valid():
            formset.save()
            #instances = formset.save(commit=False)
            #for instance in instances:
            #    instance.codProd = Prod.objects.get(pk=produto.id)
            #    instance.save()
            
            return redirect('prod.prodcomp', produto_id = produto.id)
    
    
    #formset = componentesFormSet(queryset=ProdComp.objects.filter(codProd=produto.id))
    formset = componentesFormSet(instance=produto)
    print(formset)
    
    return render(request, 'prod/componentes.html', {'formset' : formset})


def prod_list(request):
    qs = Prod.objects.only('cod', 'desc')
    
    if request.method == 'GET':
        filter = SearchProdForm(request.GET)
        qs = qs.filter(cod__istartswith = request.GET['cod'])
        if request.GET['desc']:
            dd = request.GET['desc'].split(' & ')
            for d in dd:
                qs = qs.filter(desc__icontains = d)
            print(dd)
        
        print(request)
        print(qs)   
    else:
        filter = SearchProdForm()
        print('else' + request)

    table = SearchProdTable(qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, 'prod/search_prod_form.html', {'filter': filter, 'table': table})

def prod_detail(request):
    print(request)
