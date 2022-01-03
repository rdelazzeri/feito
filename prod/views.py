from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_tables2 import SingleTableView
from django_tables2   import RequestConfig
from .models import *
from .tables import *
from .forms import *
from .filters import *
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction
from django.forms import modelformset_factory, inlineformset_factory, formset_factory

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


def prod_comp2(request, produto_id):
    print(produto_id)
    produto = Prod.objects.get(pk=produto_id) 
    componentesFormSet = inlineformset_factory(Prod, ProdComp, fk_name='codProd', form=ProdCompForm, extra=0) 
    qr = ProdComp.objects.filter(codProd=produto.id).select_related('codProd')
    if request.method == 'POST':
        #formset = componentesFormSet(request.POST, queryset=ProdComp.objects.filter(codProd=produto.id))
        formset = componentesFormSet(request.POST, request.FILES,  instance=produto.id)
        if formset.is_valid():
            formset.save()
            print('formset valido')
            return redirect('prod.prodcomp', produto_id = produto.id)
        else:
            print(formset.errors)
    else:
        formset = componentesFormSet(instance=produto, queryset = qr)
        return render(request, 'prod/componentes.html', {'formset' : formset})

def prod_comp(request, produto_id):
    produto = Prod.objects.get(pk=produto_id) 
    componentes = ProdComp.objects.filter(codProd = produto.id)
    componentesFormSet = formset_factory(ProdCompFormset, formset=BaseProdCompFormSet, extra=0)
    comp_data = [{'cod': l.codComp.cod, 'desc': l.codComp.desc, 'unid': l.codComp.unid.unid, 'qtd': l.qtd, 'codProdComp': l.id }for l in componentes] 

    if request.method == 'POST':
        comp_formset = componentesFormSet(request.POST)
        if comp_formset.is_valid():
            for comp in comp_formset:
                if id:
                    new_qtd = comp.cleaned_data.get('qtd')
                    ProdComp_id = comp.cleaned_data.get('codProdComp')
                    if ProdComp_id:
                        print('ProdComp id: ' + str(ProdComp_id))
                        ProdComp_data = ProdComp.objects.get(pk=ProdComp_id)
                        ProdComp_data.qtd = new_qtd
                        ProdComp_data.save()
            return redirect('prod:prod_comp', produto.id)
        else:
            formset = componentesFormSet(initial=comp_data)
            return render(request, 'prod/componentes.html', {'formset' : formset})
    else:
        print('não é post')
        formset = componentesFormSet(initial=comp_data)
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
                qs = qs.filter(desc__icontains = d)
    else:
        filter = SearchProdForm()

    table = SearchProdTable(qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, 'prod/search_prod_form.html', {'filter': filter, 'table': table})


def prod_search(request):
    qs = Prod.objects.only('cod', 'desc')
    if request.method == 'GET':
        filter = SearchProdForm(request.POST)
        if 'cod' in request.POST:
                    qs = qs.filter(cod__istartswith = request.POST['cod'])
        if 'desc'in request.POST:
            dd = request.POST['desc'].split(' & ')
            for d in dd:
                qs = qs.filter(desc__icontains = d)
    else:
        filter = SearchProdForm()

    table = SearchProdTable(qs)
    table.paginate(page=request.POST.get("page", 1), per_page=10)
    return render(request, 'prod/prod_search.html', {'filter': filter, 'table': table})



def prod_detail(request, prod_id):
    prod = get_object_or_404(Prod, pk=prod_id)
    if request.method == 'POST':
        print(request.POST)
        act = request.POST['act']

        print('Submit do form de produto - act: ' + str(act) + ' prod_id: ' + str(prod_id))

        if act == 'delete':
            pr = get_object_or_404(Prod, pk=prod_id)
            pr.delete()
            form = ProdDetailForm()
            return render(request, 'prod/prod_detail.html', {'form': form})
        elif act == 'save':
            print('act=save')
            #pr = get_object_or_404(Prod, pk=prod_id)
            form = ProdDetailForm(request.POST, instance = prod)
            if form.is_valid():
                print('form is valid')
                #form = ProdDetailForm(form.cleaned_data)
                form.save()
            return render(request, 'prod/prod_detail.html', {'form': form})
        elif act =='composition':
            return redirect('prod:prod_comp', prod_id)
    else:
        instance = get_object_or_404(Prod, pk=prod_id)
        print(instance)
        form = ProdDetailForm(request.POST or None, instance=instance)
        print(form)
        return render(request, 'prod/prod_detail.html', {'form': form, 'prod_id':prod_id})

    


def prod_new(request):
    if request.method == 'POST':
        form = ProdDetailForm(request.POST)
        if form.is_valid():
            pr = form.save(commit=False)
            pr.save()
            return redirect('prod_detail', prod_id=pr.pk)
        else:
            return render(request, 'prod/prod_detail.html', {'form': form})
    else:
        form = ProdDetailForm()
        return render(request, 'prod/prod_detail.html', {'form': form})

