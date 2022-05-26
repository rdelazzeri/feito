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
from django.template.loader import render_to_string
from django.http.response import HttpResponse
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from io import BytesIO
from core.relatorio_txt import *
from django.utils.safestring import mark_safe, SafeData
from datetime import datetime, timedelta







def atu_cmv():
    qr = Prod.objects.all()
    for it in qr:
        it.cmv = it.prCusto
        it.save()

def print_comp3(request, prod):
        pr = Prod.objects.get(id=prod)
        print('Árvore de produto')
        print(pr.cod, ' - ', pr.desc)
        print('Custo do produto: ', print_comp2(prod))
        return HttpResponse('feito')

def custo_composto(prod, custo, n=0):
    qr = ProdComp.objects.filter(codProd=prod)
    for it in qr:
        print('>', it.id, ' - ', it.codComp.desc, ' - ', it.codComp.cmv, ' - ', custo)
        qr2 = ProdComp.objects.filter(codProd=it.codComp)
        if qr2.count() > 0:
            for it2 in qr2:
                print('>>', it2.codComp.id, ' - ',  it2.codComp.desc, ' - ', it2.codComp.cmv, ' - ', custo)
                custo = custo_composto(it2.codComp, custo, n+1) * it2.qtd
                print(n+1)
        else:
            cmv = it.codComp.cmv if it.codComp.cmv else 0
            custo += (cmv * it.qtd)
            print('>>>', it.id, ' - ', it.codComp.desc, ' - ', custo)
    return custo


def print_comp(request, prod):
    lst=[]
    lst.insert(0, 0) 
    lst.insert(1, 0) 
    lst = print_comp2(prod, lst)
    response = []
    response.append(mark_safe(lst[1]))
    for l in lst:
        try:
            response.append(mark_safe(l['linha']))
        except:
            pass
    return render(request, 'producao/rpt.html', {'data': response})

def print_comp2(prod, pilha, nivel=0):
    qr = ProdComp.objects.filter(codProd=prod)
    custo = 0
    tab = '&nbsp;' * 3
    if qr.count() > 0:
        for it in qr:
            item = {}
            ret = []
            ret = print_comp2(it.codComp.id, pilha, nivel+1)
            print(it)
            #print('Ret[0] : ', ret[0])
            valor_unit =ret[0]
            custo += valor_unit * it.qtd
            verb = tab*nivel +  '>' + it.codComp.cod + ' - ' + it.codComp.desc + ' - ' + str(it.qtd) + ' - ' + str(valor_unit) + ' - ' + str(custo)
            
            item['cod'] = it.codComp
            item['desc'] = it.codComp.desc
            item['unid'] = it.codComp.unid
            item['qtd'] = it.qtd
            item['custo_unit'] = valor_unit
            item['custo_tot'] = custo
            item['nivel'] = nivel
            item['linha'] = verb
            #print(verb)
           
        ret.append(item)  
        return ret
    else:
        if Prod.objects.get(id = prod):
            pr = Prod.objects.get(id = prod)
            custo = pr.cmv if pr.cmv else 0
            pilha[0] = custo
            pilha[1] += custo
            verb = tab*nivel +  '>' + pr.cod + ' - ' + pr.desc + ' - ' + str(valor_unit) + ' - ' + str(custo)
            item['linha'] = verb
            pilha.append()
        else:
            pilha[0] = 0
        return pilha



def produto_search(request):
    data = dict()    
    if request.method == 'GET':
        pesq = request.GET.get('pesquisa')
        tipo = request.GET.get('tipo') if request.GET.get('tipo') else None
        tipo = None if tipo == 'CO' else tipo
        print(tipo)
        prods = Prod.objects.only('id', 'cod', 'desc').filter(desc__istartswith = pesq)
        prods = prods.filter(tipoProduto__cod = tipo) if tipo else prods
        prods = prods.exclude(tipoProduto__cod = 'SI') if tipo == None else prods
        prods = prods.exclude(tipoProduto__cod = 'SE') if tipo == None else prods

        data['table'] = render_to_string(
            'prod/_prod_table.html',   
            {'prods': prods},
        )
        print('Pesquisa: ' + pesq)
        return HttpResponse(data['table'])
    else:
        print('Prod search - ' + request.POST)
        return render(request, 'prod/produto_search.html' )



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
        #print(request.POST)
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
        #print(instance)
        form = ProdDetailForm(request.POST or None, instance=instance)
        #print(form)
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

