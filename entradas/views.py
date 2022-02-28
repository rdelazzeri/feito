from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.http.response import HttpResponse
from django.forms import formset_factory
from .models import *
from .forms import *
from django.db import transaction
from financeiro.models import Vencimento

def nf_entrada_list(request):
    lista = NF_entrada.objects.all()
    return render(request, 'entradas/nf_entrada_list.html', {'lista': lista})


def nf_entrada_new(request):
    print('nf_entrada_new/00')
    if request.method == "POST":
        print('nf_entrada_new/01')
        form = NF_entrada_detail_form(request.POST)
        if form.is_valid():
            print('nf_entrada_new/02')
            fr = form.save(commit=False)
            fr.save()
            return redirect('entradas:nf_entrada_detail', fr.id) 
        else:
            print('nf_entrada_new/03')
            return render(request, 'entradas/nf_entrada_detail.html', {'form': form})     
    else:
        print('nf_entrada_new/ 10')
        form = NF_entrada_detail_form()
        return render(request, 'entradas/nf_entrada_detail.html', {'form': form})   


class NomeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print('nome-autocomplete')
        if not self.request.user.is_authenticated:
            return Parceiro.objects.none()
        qs = Parceiro.objects.only('nome')
        if self.q:
            qs = qs.filter(nome__icontains=self.q)
        return qs

class TransportadoraAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print('transportadora-autocomplete')
        if not self.request.user.is_authenticated:
            return Parceiro.objects.none()
        qs = Parceiro.objects.filter(tipo__sigla = 'T').only('nome')
        if self.q:
            qs = qs.filter(nome__icontains=self.q)
        return qs

def nf_entrada_prod_search(request):
    data = dict()    
    if request.method == 'GET':
        pesq = request.GET.get('pesquisa')
        prod = Prod.objects.only('id', 'cod', 'desc').filter(desc__istartswith = pesq)
        data['table'] = render_to_string(
            'comercial/_prod_table.html',   
            {'prods': prod},
        )
        print('Pesquisa: ' + pesq)
        return HttpResponse(data['table'])
    else:
        print('Prod search - ' + request.POST)
        return render(request, 'comercial/orcamento_prod_search.html' )


def nf_entrada_read(request, id):
    pass

@transaction.atomic
def nf_entrada_item_add(request):
    if request.method == 'GET':
        produto = request.GET.get('produto')
        id = request.GET.get('id')
        print(produto)
        print(id)
        nf = NF_entrada.objects.get(pk=id)
        prod = Prod.objects.get(pk=produto)
        nf_it = NF_entrada_itens()
        nf_it.nf_entrada = nf
        nf_it.produto = prod
        nf_it.save()

        return HttpResponse('Produto adicionado')
    else:
        return HttpResponse('nao é post')

def nf_entrada_parcelas_create(request):
    id = request.GET.get('id')
    print(id)
    nf = NF_entrada.objects.get(id = id)
    parcelas = Vencimento.objects.parcelas_create(nf.vencimento, nf.valor_total_nota, nf.data_emissao)
    print (parcelas)
    for p in parcelas:
        print(p)
        cp = Conta_pagar()
        cp.entrada = nf
        cp.nf = nf.num
        cp.parcela_num = p['numero']
        cp.data_emissao = nf.data_emissao
        cp.vencimento = p['vencimento']
        cp.valor_parcela = p['valor_parcela']
        cp.conta_caixa = nf.operacao.conta_caixa
        cp.save()
        
    formset_parc = formset_parcelas(nf = nf)
    data = dict()    
    data['table'] = render_to_string(
        'entradas/nf_entrada_parcelas_table.html',   
        {'formset_parcelas': formset_parc},
    )
    return HttpResponse(data['table'])
    

def nf_entrada_parcelas_delete(request):
    id = request.GET.get('id')
    Conta_pagar.objects.filter(entrada_id = id).delete()
    nf = NF_entrada.objects.get(id = id)
    formset_parc = formset_parcelas(nf = nf)
    data = dict()    
    data['table'] = render_to_string(
        'entradas/nf_entrada_parcelas_table.html',   
        {'formset_parcelas': formset_parc},
    )
    return HttpResponse(data['table'])


def nf_entrada_item_delete(request):
    id_item = request.GET.get('item_id')
    it = NF_entrada_itens.objects.get(pk=id_item)
    it.delete()
    return HttpResponse('Produto excluido')


def nf_entrada_delete(request):
    id = request.GET.get('id')
    nf = NF_entrada.objects.get(pk=id)
    nf.delete()

    #NF_entrada.objects.filter(pk=id).delete()
    return redirect('entradas:nf_entrada_list')

def formset_parcelas(**kwargs):
    nf_parcelas_formset = formset_factory(NF_entrada_parcelas_formset, NF_entrada_parcelas_BaseFormSet, extra=0)
    if kwargs.get('nf'):
        nf = kwargs.get('nf')
        nf_parcelas = nf.parcelas.all()
        nf_parcelas_initial = [{
            'parc_id': l.id,
            'num': l.parcela_num,
            'venc': l.vencimento,
            'valor': l.valor_parcela,  
            }for l in nf_parcelas] 
        formset_parcelas = nf_parcelas_formset(initial = nf_parcelas_initial)
        return formset_parcelas
    if kwargs.get('request'):
        request = kwargs.get('request')
        formset_parcelas = nf_parcelas_formset(request)
        if formset_parcelas.is_valid():
            print('formset_parcelas válido')
            for p in formset_parcelas:
                parc_id = p.cleaned_data.get('parc_id')
                parc_data = Conta_pagar.objects.get(id=parc_id)
                parc_data.vencimento = p.cleaned_data.get('venc')
                parc_data.valor_parcela = p.cleaned_data.get('valor')
                parc_data.save()
                print(parc_data.entrada)
                print(p.cleaned_data.get('venc'))
            return True
        else:
            return False

def nf_entrada_detail(request, pk):
    nf = get_object_or_404(NF_entrada, pk=pk)
    nf_itens = NF_entrada_itens.objects.filter(nf_entrada = nf)
    nf_itens_formset = formset_factory(NF_entrada_itens_formset, NF_entrada_itens_BaseFormSet, extra=0 )    
    nf_itens_initial = [{
        'item_id': l.id,
        'cod': l.produto.cod,
        'desc': l.produto.desc, 
        'unid': l.produto.unid.unid, 
        'qtd': l.qtd, 
        'preco_unit': l.preco_unit, 
        'preco_tot':l.preco_tot,
        'aliq_icms': l.aliq_icms,
        'aliq_ipi': l.aliq_ipi,
        'valor_icms': l.valor_icms,
        'valor_ipi': l.valor_ipi,
        'valor_total_item': l.valor_total_item, 
        }for l in nf_itens] 
    formset = nf_itens_formset(initial = nf_itens_initial)    
    formset_parc = formset_parcelas(nf = nf)

    if request.method == 'POST':
        print('é post')
        form = NF_entrada_detail_form(request.POST, instance = nf)
        formset = nf_itens_formset(request.POST)
        
        if form.is_valid():
            print('form is valid')
            if formset.is_valid():
                print('formset is valid')
                nf = form.save(commit=False)
                nf.save()
                for it in formset:
                    if id:
                        item_id = it.cleaned_data.get('item_id')
                        #print(it.cleaned_data)
                        if item_id:
                            itens_data = NF_entrada_itens.objects.get(pk=item_id)
                            itens_data.qtd = it.cleaned_data.get('qtd')
                            itens_data.preco_unit = it.cleaned_data.get('preco_unit')
                            itens_data.aliq_icms = it.cleaned_data.get('aliq_icms')
                            itens_data.aliq_ipi = it.cleaned_data.get('aliq_ipi')
                            itens_data.save()

                if formset_parcelas(request = request.POST):    
                    return redirect('entradas:nf_entrada_detail', nf.id)
                else:
                    print('erro em formset parcelas')
            else:
                print(formset.non_form_errors())
            
    else:
        form = NF_entrada_detail_form(instance  = nf)
    return render(request, 'entradas/nf_entrada_detail.html', {'form': form, 'formset': formset, 'formset_parcelas': formset_parc, 'id': nf.id})












def oc_list(request):
    pass

def oc_new(request):
    pass

def oc_detail(request, pk):
    pass

def sm_list(request):
    pass

def sm_new(request):
    pass

def sm_detail(request, pk):
    pass