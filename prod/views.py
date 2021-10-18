from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
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
        if 'cod' in request.GET:
                    qs = qs.filter(cod__istartswith = request.GET['cod'])
        if 'desc'in request.GET:
            dd = request.GET['desc'].split(' & ')
            for d in dd:
                print(d)
                qs = qs.filter(desc__icontains = d)
    else:
        filter = SearchProdForm()


    table = SearchProdTable(qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, 'prod/search_prod_form.html', {'filter': filter, 'table': table})

def prod_detail(request, prod_id):
    if request.method == 'POST':
        form = ProdDetailForm(request.POST or None)
        if form.is_valid():
            form = ProdDetailForm(form.cleaned_data)
            form.save()
           
            
    else:
        if prod_id != '0':
            instance = get_object_or_404(Prod, pk=prod_id)
            #instance = Prod.objects.get(id=prod_id)
            form = ProdDetailForm(request.POST or None, instance=instance)
        else:
            form = ProdDetailForm()

    return render(request, 'prod/prod_detail.html', {'form': form})


def prod_new(request):
    if request.method == 'POST':
        form = ProdDetailForm(request.POST or None)
        if form.is_valid():
            form = ProdDetailForm(form.cleaned_data)
            form.save()
            return redirect('prod_detail', prod_id=form.pk)
    else:
        form = ProdDetailForm()
        return render(request, 'prod/prod_detail.html', {'form': form})

