#from django.contrib.auth.models import User
#from django.forms.formsets import formset_factory
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from financeiro.models import Conta_receber, Vencimento
#from django_tables2 import SingleTableView
#from django_tables2   import RequestConfig
from .models import  Orcamento, Orcamento_item, Pedido, Pedido_item, Comercial_config, Entrega, Entrega_item, Entrega_parcelas
from .tables import *
from .forms import *
#from .filters import *
#from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
#from django.db import transaction
#from django.forms import modelformset_factory, inlineformset_factory, formset_factory
#from django_filters.views import FilterView
#from django_tables2.views import SingleTableMixin
from bootstrap_modal_forms.generic import BSModalCreateView
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from fiscal.models import *
from django.db import transaction
from fiscal.services import *
import datetime
from datetime import datetime, date
from django.utils.timezone import now
from contextlib import suppress
from django.utils.safestring import mark_safe
from django.apps import apps
from io import BytesIO
from reports.reports import Label_volumes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
) 



class Pedido_filter(BSModalFormView):
    template_name = 'comercial/pedido_filter.html'
    form_class = PedidoFilterForm

    def form_valid(self, form):
        self.filter = '?type=' + form.cleaned_data['type']
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('comercial:pedidos_list') + self.filter

class Pedido_create(BSModalCreateView):
    template_name = 'comercial/pedido_create.html'
    form_class = PedidoModelForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('comercial:pedidos_list')
  

class Pedido_update(BSModalUpdateView):
    model = Pedido
    template_name = 'comercial/pedido_update.html'
    form_class = PedidoModelForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('comercial:pedidos_list')

class Pedido_delete(BSModalDeleteView):
    model = Pedido
    template_name = 'comercial/pedido_delete.html'
    success_message = 'Pedido Excluído.'
    success_url = reverse_lazy('comercial:pedidos_list')



class Pedido_add_item(BSModalCreateView):
    template_name = 'comercial/pedido_add_item.html'
    form_class = PedidoItemModelForm
    success_message = 'Success: Book was created.'
    #success_url = reverse_lazy('comercial:pedido')


def pedidos_list(request):
    ped = Pedido.objects.all()
    table = PedidosTable(ped)
    table.paginate(page=request.GET.get("page", 1), per_page=2)
    return render(request, 'comercial/pedidos_list.html', {'table': table, 'pedidos': ped})
  
def pedidos(request):
    data = dict()
    if request.method == 'GET':
        ped = Pedido.objects.all()
        data['table'] = render_to_string(
            'comercial/_pedidos_table.html',
            {'pedidos': ped},
            request=request
        )
        return JsonResponse(data)

def pedido_detail(request, ped_id):
    ped = Pedido.objects.get(pk=ped_id)
    if request.method == "POST":
        form = PedidoDetailForm(request.POST, ped)
        if form.is_valid():
            ped = form.save(commit=False)
            ped.save()
            return redirect('comercial:pedidos_list')       
    else:
        form = PedidoDetailForm(instance=ped)
        return render(request, 'comercial/pedido_detail.html', {'form': form, 'pedido_id': ped})

class Pedido_read(BSModalReadView):
    model = Pedido
    template_name = 'comercial/pedido_read.html'

#--------------------------------------
#
#orçamento
#
#--------------------------------------

def orcamento_new(request):
    print('orcamento_new/00')
    if request.method == "POST":
        print('pedido_new/01')
        form = OrcamentoDetailForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('orcamento_new/02')
            orc = form.save(commit=False)
            orc.save()
            return redirect('comercial:orcamento_detail', orc.id) 
        else:
            print('orcamento_new/03')
            print(form)
            return render(request, 'comercial/orcamento_detail.html', {'form': form})     
    else:
        print('orcamento_new 10')
        new = Orcamento()
        cfg = Comercial_config.objects.get(pk=1)
        new.num_orc = cfg.num_ult_orcamento + 1
        new.save()
        cfg.num_ult_orcamento = new.num_orc
        cfg.save()
        return redirect('comercial:orcamento_detail', new.id)
        #form = OrcamentoDetailForm()
        #return render(request, 'comercial/orcamento_detail.html', {'form': form})

def orcamento_list(request):
    orc = Orcamento.objects.all()
    #table = PedidosTable(orc)
    #table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, 'comercial/orcamento_list.html', {'orcamentos': orc})



def orcamento_detail(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, pk=orcamento_id)
    orcamento_itens = Orcamento_item.objects.filter(orcamento = orcamento.id)
    orcamento_itens_formset = formset_factory(Orcamento_itens_formset, Orcamento_itens_BaseFormSet, extra=0 )    
    orcamento_itens_initial = [{
        'item_id': l.id,
        'cod': l.produto.cod,
        'desc': l.produto.desc, 
        'unid': l.produto.unid.unid, 
        'qtd': l.qtd, 
        'pr_unit': l.pr_unit, 
        'pr_tot':l.pr_tot, 
        'obs':l.obs
        }for l in orcamento_itens] 
    
    formset = orcamento_itens_formset(initial = orcamento_itens_initial)

    if request.method == 'POST':
        print('é post')
        form = OrcamentoDetailForm(request.POST, instance = orcamento)
        formset = orcamento_itens_formset(request.POST)
        if form.is_valid():
            print('form is valid')
            if formset.is_valid():
                print('formset is valid')
                orcamento = form.save(commit=False)
                orcamento.save()
                for it in formset:
                    if id:
                        new_qtd = it.cleaned_data.get('qtd')
                        item_id = it.cleaned_data.get('item_id')
                        codigo = item_id
                        print(item_id)
                        print(it.cleaned_data)
                        if item_id:
                            itens_data = Orcamento_item.objects.get(pk=item_id)
                            itens_data.qtd = new_qtd
                            itens_data.pr_unit = it.cleaned_data.get('pr_unit')
                            itens_data.save()
                return redirect('comercial:orcamento_detail', orcamento.id)
            else:
                print(formset.non_form_errors())
            
    else:
        form = OrcamentoDetailForm(instance  = orcamento)
        print(request.GET)
    return render(request, 'comercial/orcamento_detail.html', {'form': form, 'formset': formset, 'orcamento_id': orcamento.id})

def orcamento_prod_search(request):
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
        return HttpResponse('oi')
    else:
        print('Prod search - ' + request.POST)
        return render(request, 'comercial/orcamento_prod_search.html' )

def orcamento_item_add(request):
    if request.method == 'GET':
        produto = request.GET.get('produto')
        orcamento = request.GET.get('orcamento')
        print(produto)
        print(orcamento)
        orc = Orcamento.objects.get(pk=orcamento)
        prod = Prod.objects.get(pk=produto)
        orc_it = Orcamento_item()
        orc_it.orcamento = orc
        orc_it.produto = prod
        orc_it.save()

        return HttpResponse('Produto adicionado')
    else:
        return HttpResponse('nao é post')

def orcamento_delete(request):
    orcamento_id = request.GET.get('orcamento_id')
    Orcamento.objects.filter(pk=orcamento_id).delete()
    orcamento_id = int(orcamento_id) - 1
    print(orcamento_id)
    return redirect('comercial:orcamento_list')


def orcamento_item_delete(request):
    orcamento_item = request.GET.get('item_id')
    it = Orcamento_item.objects.get(pk=orcamento_item)
    it.delete()
    return HttpResponse('Produto excluido')

@transaction.atomic
def orcamento_pedido_add(request):
    orcamento_id = request.GET.get('orcamento_id')
    print(orcamento_id)
    orc = Orcamento.objects.get(pk=orcamento_id)
    cfg = Comercial_config.objects.get(pk=1)
    novo_num = cfg.num_ult_pedido + 1
    cfg.num_ult_pedido = novo_num
    cfg.save()
    print(novo_num)
    ped_new = Pedido()
    ped_new.num = novo_num
    print(ped_new.num)
    ped_new.operacao = orc.operacao
    ped_new.status__id = 1
    ped_new.data_cadastro = '2021-12-16'
    ped_new.data_previsao =  orc.data_previsao   #datetime.now() + datetime.timedelta(days=orc.prazo_entrega)
    ped_new.cliente = orc.cliente
    ped_new.vencimentos = orc.vencimentos
    ped_new.transportadora = orc.transportadora
    ped_new.tipo_frete = orc.tipo_frete
    ped_new.valor_frete = orc.valor_frete
    ped_new.obs = orc.obs
    ped_new.save()
    print(ped_new.id)

    itens = Orcamento_item.objects.filter(orcamento__id = orc.id)
    print(itens)
    for item in itens:
        print('entrei no for')
        ped_new_item = Pedido_item()
        print('instanciei o pedido item')
        ped_new_item.pedido = ped_new
        ped_new_item.produto = item.produto
        ped_new_item.qtd = item.qtd
        ped_new_item.pr_unit = item.pr_unit
        ped_new_item.obs = item.obs
        ped_new_item.save()

    #return JsonResponse({'pedido_id': ped_new.id})
    return redirect('comercial:pedido_full', ped_new.id)

#--------------------------------------
#
#pedido
#
#--------------------------------------
def pedido_new(request):
    print('pedido_new/00')
    if request.method == "POST":
        print('pedido_new/01')
        form = PedidoDetailForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('pedido_new/02')
            ped = form.save(commit=False)
            ped.save()
            #return render(request, 'comercial/pedido_detail_full.html', {'form': form})
            return redirect('comercial:pedido_full', ped.id) 
        else:
            print('pedido_new/03')
            print(form)
            return render(request, 'comercial/pedido_detail_full.html', {'form': form})     
    else:
        print('pedido_new/04')
        form = PedidoDetailForm()
        return render(request, 'comercial/pedido_detail_full.html', {'form': form})


def pedidos_prod_search(request):
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
        return HttpResponse('oi')
    else:
        print('Prod search - ' + request.POST)
        return render(request, 'comercial/prod_search.html' )


def pedido_item_add(request):
    if request.method == 'POST':
        produto = request.POST.get('produto')
        pedido = request.POST.get('pedido')
        print(produto)
        print(pedido)
        ped = Pedido.objects.get(pk=pedido)
        prod = Prod.objects.get(pk=produto)
        ped_it = Pedido_item()
        ped_it.pedido = ped
        ped_it.produto = prod
        ped_it.save()

        return HttpResponse('Produto adicionado')
    else:
        return HttpResponse('nao é post')


def pedidos_prod_search_table(request):
    data = dict()   
    if request.method == 'GET':
        prod = Prod.objects.only('cod', 'desc').filter(desc__istartswith = 'COLUNA 210')
        data['table'] = render_to_string(
            'comercial/_prod_table.html',
            {'produtos': prod},
        )
        return JsonResponse(data)


def pedido_item_delete(request):
    if request.method == 'POST':
        pedido_item = request.GET.get('item_id')
        it = Pedido_item.objects.get(pk=pedido_item)
        it.delete()
        return HttpResponse('Produto excluido')
    else:
        return False

def pedido_full(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    pedido_itens = Pedido_item.objects.filter(pedido = pedido.id)
    pedido_itens_formset = formset_factory(Pedido_itens_formset, Pedido_itens_BaseFormSet, extra=0 )    
    pedido_itens_initial = [{
        'item_id': l.id,
        'cod': l.produto.cod,
        'desc': l.produto.desc, 
        'unid': l.produto.unid.unid, 
        'qtd': l.qtd, 
        'pr_unit': l.pr_unit, 
        'pr_tot':l.pr_tot, 
        'qtd_entregue':l.qtd_entregue,
        'val_entregue':l.val_entregue,
        'qtd_saldo':l.qtd_saldo,
        'valor_saldo':l.valor_saldo
        }for l in pedido_itens] 
    
    formset = pedido_itens_formset(initial = pedido_itens_initial)

    if request.method == 'POST':
        print('é post')
        form = PedidoDetailForm(request.POST, instance = pedido)
        formset = pedido_itens_formset(request.POST)
        if form.is_valid():
            print('form is valid')
            if formset.is_valid():
                print('formset is valid')
                pedido = form.save(commit=False)
                pedido.save()
                for it in formset:
                    if id:
                        new_qtd = it.cleaned_data.get('qtd')
                        item_id = it.cleaned_data.get('item_id')
                        codigo = item_id
                        print(item_id)
                        print(it.cleaned_data)
                        if item_id:
                            itens_data = Pedido_item.objects.get(pk=item_id)
                            itens_data.qtd = new_qtd
                            itens_data.pr_unit = it.cleaned_data.get('pr_unit')
                            itens_data.save()
                return redirect('comercial:pedido_full', pedido.id)
            else:
                print(formset.non_form_errors())
            
    else:
        form = PedidoDetailForm(instance  = pedido)
        print(request.GET)
    return render(request, 'comercial/pedido_detail_full.html', {'form': form, 'formset': formset, 'pedido_id': pedido.id})


@transaction.atomic
def pedido_entrega_add(request):
    print('comercial.view.entrega_add')
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        print(pedido_id)
        pedido = Pedido.objects.get(pk=pedido_id)
        cfg = Comercial_config.objects.get(pk=1)
        novo_num = cfg.num_ult_entrega + 1
        cfg.num_ult_entrega = novo_num
        cfg.save()
        print(novo_num)
        entrega_new = Entrega()
        entrega_new.num = novo_num
        entrega_new.pedido_origem = pedido
        print(entrega_new.num)
        entrega_new.operacao = pedido.operacao
        entrega_new.status__id = 1
        entrega_new.data_cadastro = date.today()
        entrega_new.data_emissao =  date.today()
        entrega_new.cliente = pedido.cliente
        entrega_new.vencimentos = pedido.vencimentos
        entrega_new.transportadora = pedido.transportadora
        entrega_new.tipo_frete = pedido.tipo_frete
        entrega_new.valor_frete = pedido.valor_frete
        entrega_new.obs = pedido.obs
        entrega_new.save()
        print(entrega_new.id)

        itens = Pedido_item.objects.filter(pedido_id = pedido.id)
        valtot = 0
        print(itens)
        for item in itens:
            print('entrei no for')
            entrega_new_item = Entrega_item()
            print('instanciei o pedido item')
            entrega_new_item.entrega = entrega_new
            entrega_new_item.pedido_item = item
            entrega_new_item.produto = item.produto
            entrega_new_item.qtd = item.qtd_saldo
            entrega_new_item.pr_unit = item.pr_unit
            entrega_new_item.obs = item.obs
            entrega_new_item.pr_tot = Decimal(item.qtd) * Decimal(item.pr_unit)
            valtot += entrega_new_item.pr_tot
            entrega_new_item.save()
        
        entrega_new.valor_total_produtos = Decimal(valtot)
        entrega_new.valor_total_entrega = Decimal(valtot) + Decimal(entrega_new.valor_frete)
        entrega_new.save()

        return JsonResponse({'entrega_id': entrega_new.id})
    else:
        return JsonResponse({'entrega_id': 'erro'})






#--------------------------------------
#
#entrega
#
#--------------------------------------

def entrega_new(request):
    print('entrega_new/00')
    if request.method == "POST":
        print('pedido_new/01')
        form = EntregaDetailForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('entrega_new/02')
            orc = form.save(commit=False)
            orc.save()
            return redirect('comercial:entrega_detail', orc.id) 
        else:
            print('entrega_new/03')
            print(form)
            return render(request, 'comercial/entrega_detail.html', {'form': form})     
    else:
        new = Entrega()
        cfg = Comercial_config.objects.get(pk=1)
        new.num = cfg.num_ult_entrega + 1
        new.save()
        cfg.num_ult_entrega = new.num
        cfg.save()
        return redirect('comercial:entrega_detail', new.id)
        #form = entregaDetailForm()
        #return render(request, 'comercial/entrega_detail.html', {'form': form})

def entrega_list(request):
    ent= Entrega.objects.all().select_related('pedido_origem').order_by('-num')
    paginator = Paginator(ent, 40) # Show 25 contacts per page.
    
   
    page_number = request.GET.get('page', 1)

   
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    #table = PedidosTable(orc)
    #table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, 'comercial/entrega_list.html', {'page_obj': page_obj})



def entrega_detail(request, entrega_id):
    entrega = get_object_or_404(Entrega, pk=entrega_id)
    cliente_id = entrega.cliente_id
    entrega_itens = Entrega_item.objects.select_related('pedido_item__pedido').filter(entrega = entrega.id)
    entrega_itens_formset = formset_factory(Entrega_itens_formset, Entrega_itens_BaseFormSet, extra=0 )
    parcelas = Entrega_parcelas.objects.filter(entrega=entrega)    
    p = ''
    for parc in parcelas:
        dt = parc.vencimento
        vc = dt.strftime('%d/%m/%y')
        p = p + 'Venc.: ' + vc + ' Val.: ' + str(parc.valor_parcela) + '\n'

    entrega_itens_initial = [{
                'item_id': item.id,
                'pedido': item.pedido_item.pedido.num,
                'cod': item.produto.cod,
                'desc': item.produto.desc, 
                'unid': item.produto.unid.unid, 
                'qtd': item.qtd, 
                'pr_unit': item.pr_unit, 
                'pr_tot':item.pr_tot, 
                'obs':item.obs,
                'ncm': item.produto.ncm.cod
                }for item in entrega_itens]
    
    formset = entrega_itens_formset(initial = entrega_itens_initial)

    if request.method == 'POST':
        print('é post')
        #verifica se já existe uma nota emitida e aprovada
        pre_nota = Pre_nota.objects.filter(entrega = entrega).first()
        
        if pre_nota:
            #print('pre_nota: ' + str(pre_nota.count()))
            ret = NFe_transmissao.objects.filter(pre_nota = pre_nota).first()
            print('status da transmissao: ' + str(ret.status))

            if ret.erro():
                print('NFe não aprovada')
        form = EntregaDetailForm(request.POST, instance = entrega)
        formset = entrega_itens_formset(request.POST)
        #print(formset)
        if form.is_valid():
            print('form is valid')
            if formset.is_valid():
                print('formset is valid')
                entrega = form.save(commit=False)
                entrega.save()
                for it in formset:
                    if id:
                        new_qtd = it.cleaned_data.get('qtd')
                        item_id = it.cleaned_data.get('item_id')
                        codigo = item_id
                        print(it.cleaned_data)
                        if item_id:
                            itens_data = Entrega_item.objects.get(pk=item_id)
                            itens_data.qtd = new_qtd
                            itens_data.pr_unit = it.cleaned_data.get('pr_unit')
                            #atualiza NCM do produto direto da tela da entrega
                            #tem que digitar o código correspondente na tabela
                                                            
                            ncm_cod = it.cleaned_data.get('ncm')
                            print(ncm_cod)

                            try:
                                print('entrei no try do ncm')
                                ncm = NCM.objects.get(cod = ncm_cod)
                                print(ncm.cod)
                                itens_data.produto.ncm = ncm
                            except:
                                ncm = NCM()
                                ncm.cod = ncm_cod
                                ncm.save()
                                itens_data.produto.ncm = ncm

                            itens_data.save()
                            itens_data.produto.save()

                return redirect('comercial:entrega_detail', entrega.id)
            else:
                print(formset.non_form_errors())
                
    
    form = EntregaDetailForm(instance  = entrega)
    print(entrega.id)
    return render(request, 'comercial/entrega_detail.html', {'form': form, 'formset': formset, 'entrega_id': entrega.id, 'cliente_id': cliente_id, 'parcelas': p})


def pre_nota_retorno(request):
    print('Consultando retorno')
    if request.method == 'GET' and request.is_ajax:
        entrega_id = request.GET.get('entrega_id')
        pre_nota = Pre_nota.objects.filter(entrega_id = entrega_id).first()
        print(pre_nota.id)
        ret = NFe_transmissao.objects.filter(pre_nota_id = pre_nota.id).first()
        #print(ret)
        form = EntregaRetornoForm(instance=ret)
        #print(form)
        danfe = ret.danfe
        xml = ret.xml
        data = render_to_string('comercial/entrega_retorno.html', {'form': form, 'ret': ret, 'danfe': danfe, 'xml': xml})
        print(data)
        return HttpResponse(data)


def entrega_prod_search(request):
    data = dict()    
    if request.method == 'GET':
        pesq = request.GET.get('pesquisa')
        cliente_id = request.GET.get('cliente_id')
        print('Cliente id: ' + cliente_id + 'Pesquisa: ' + pesq)
        #prod = Prod.objects.only('id', 'cod', 'desc').filter(desc__istartswith = pesq)
        prods = Pedido_item.objects.select_related('produto', 'pedido__cliente').filter(pedido__cliente_id = cliente_id)
        prods = prods.filter(valor_saldo__gt = 0)
        prods = prods.filter(produto__desc__icontains = pesq)
        print('Descricao: ' + prods[0].produto.desc)

        data['table'] = render_to_string(
            'comercial/entrega_prod_search_table.html',   
            {'prods': prods},
        )
        print('Pesquisa: ' + pesq)
        return HttpResponse(data['table'])
        return HttpResponse('oi')
    else:
        print('Prod search - ' + request.POST)
        return render(request, 'comercial/entrega_prod_search.html' )

def entrega_item_add(request):
    if request.method == 'POST':
        orc = Entrega.objects.get(pk=request.GET.get('entrega_id'))
        prod = Prod.objects.get(pk=request.GET.get('produto_id'))
        orc_it = Entrega_item()
        orc_it.entrega = orc
        orc_it.produto = prod
        orc_it.save()

        return HttpResponse('Produto adicionado')
    else:
        return HttpResponse('nao é post')

def entrega_delete(request):
    if request.method == 'POST':
        entrega_id = request.POST.get('entrega_id')
        Entrega.objects.filter(pk=entrega_id).delete()
        entrega_id = int(entrega_id) - 1
        print(entrega_id)
        return redirect('comercial:entrega_list')
    else:
        return False

def entrega_item_delete(request):
    if request.method == 'POST':
        entrega_item = request.POST.get('item_id')
        it = Entrega_item.objects.get(pk=entrega_item)
        it.delete()
        return HttpResponse('Produto excluido')
    else:
        return False

@transaction.atomic
def pre_nota_add(request):
    print('comercial.views.pre_nota_add')
    if request.method == 'POST':
        print('Iniciando processamento da NFe')
        entrega_id = request.POST.get('entrega_id')
        print('entrega_id: ' + str(entrega_id))
        entrega = Entrega.objects.get(pk=entrega_id)
        print('Número da NF: ' + str(entrega.num_nf))

        #verifica se já existe uma nota emitida e aprovada
        pre_nota = Pre_nota.objects.filter(entrega = entrega).first()
        ret = NFe_transmissao.objects.filter(pre_nota = pre_nota).first()
        if ret:
            if ret.status == 'aprovado': 
                print('nf já emitida e aprovada')
                return HttpResponse('Nota fiscal já emitida')

        #se não tiver nota aprovada, pode sobreescrever a pre-nota
        itens = Entrega_item.objects.filter(entrega_id = entrega_id)
        cfg = NF_config.objects.filter(pk = 1).first()
                
        if entrega.num_nf == 0:
            print(cfg.last_num)
            cfg.last_num = cfg.last_num + 1
            num_nf = cfg.last_num
            print('número da nota fiscal' + str(num_nf))
            cfg.save()
            entrega.num_nf = num_nf
            entrega.save()
        else:
            num_nf = entrega.num_nf
        
        try:
            print('Verificando se já existe pré-nota gravada')
            pnf = Pre_nota.objects.get(entrega = entrega)
            print('número da pre_nota: ' + str(pnf.id))
            #Flag indicando uma emissão de correcao/ajuste de nf reprovada
            correcao = True
        except:
            print('nenhuma pre-nota encontrada')
            pnf = Pre_nota()
            pnf.entrega = entrega
            #Flag indicando uma primeira emissao da nota
            correcao = False

        pnf.num_nf = num_nf
        pnf.operacao = entrega.operacao.tipo
        pnf.data_emissao = entrega.data_emissao
        pnf.natureza_operacao = entrega.operacao.natureza_operacao
        pnf.modelo = '1' # 1 - NF-e - 2 - NFC-e
        pnf.finalidade = entrega.operacao.finalidade
        pnf.ambiente = cfg.ambiente
        pnf.url_notificacao = cfg.url_notificacao
        #pnf.classe_imposto = entrega.operacao.classe_imposto
        pnf.save()
        
        #Pre_nota_cliente
        if correcao: 
            pnf_cli = Pre_nota_cliente.objects.filter(pre_nota = pnf).first()
            if pnf_cli:
                print('Atualizando - Pnf_cli: ' + str(pnf_cli.id))
            else:
                pnf_cli = Pre_nota_cliente()
                print('Criando - Pnf_cli: ' + str(pnf_cli.id))
        else:
            pnf_cli = Pre_nota_cliente()
            print('Criando - Pnf_cli: ' + str(pnf_cli.id))

        pnf_cli.pre_nota = pnf
        pnf_cli.cpf = entrega.cliente.cpf
        pnf_cli.nome_completo = entrega.cliente.nome
        pnf_cli.cnpj = entrega.cliente.cnpj
        pnf_cli.razao_social = entrega.cliente.nome
        pnf_cli.ie = entrega.cliente.insc_est
        pnf_cli.suframa = entrega.cliente.suframa
        pnf_cli.substituto_tributario = ''
        pnf_cli.consumidor_final = ''
        pnf_cli.contribuinte = ''
        pnf_cli.microcervejaria = False
        pnf_cli.endereco = entrega.cliente.logradouro
        pnf_cli.complemento = entrega.cliente.complemento
        pnf_cli.numero = entrega.cliente.numero
        pnf_cli.bairro = entrega.cliente.bairro
        pnf_cli.cidade = entrega.cliente.cidade
        pnf_cli.uf = entrega.cliente.estado
        pnf_cli.cep = entrega.cliente.cep
        pnf_cli.telefone = entrega.cliente.fone1
        pnf_cli.email = entrega.cliente.email_nfe
        pnf_cli.save()

        #produtos
        itens = Entrega_item.objects.filter(entrega=entrega)
        Pre_nota_produtos.objects.filter(pre_nota=pnf).delete()
        for item in itens:
            pnf_prod = Pre_nota_produtos()
            pnf_prod.pre_nota = pnf
            pnf_prod.produto_id = 0
            pnf_prod.item = 0
            pnf_prod.nome = item.produto.desc
            pnf_prod.codigo = item.produto.cod
            pnf_prod.ncm = item.produto.ncm
            pnf_prod.quantidade = item.qtd
            #pnf_prod.quantidade_tributavel = ''
            pnf_prod.unidade = item.produto.unid.unid
            #pnf_prod.unidade_tributavel = ''
            pnf_prod.peso = 0
            pnf_prod.origem = item.produto.origemFiscal
            pnf_prod.desconto = 0
            pnf_prod.subtotal = item.pr_unit
            pnf_prod.subtotal_tributavel = item.pr_unit
            pnf_prod.total = item.pr_tot
            #pnf_prod.classe_imposto = ''
            #pnf_prod.cest = ''
            #pnf_prod.beneficio_fiscal = ''
            pnf_prod.informacoes_adicionais = item.inf_adic
            #pnf_prod.gtin = ''
            #pnf_prod.gtin_tributavel = ''
            #pnf_prod.cod_barras = ''
            #pnf_prod.cod_barras_tributavel = ''
            #pnf_prod.nve = ''
            #pnf_prod.nrecopi = ''
            pnf_prod.ativo_permanente = False
            #pnf_prod.veiculo_usado = ''
            #pnf_prod.ex_ipi = ''
            pnf_prod.classe_imposto = entrega.operacao.classe_imposto
            pnf_prod.save()

            mov = {}
            mov['data'] = entrega.data_emissao
            mov['desc'] = 'ENTREGA: %s Saída mercadoria' %(entrega.num)
            mov['produto'] = item.produto
            mov['qtd_entrada'] = 0
            mov['qtd_saida'] = item.qtd
            mov['valor'] = item.produto.cmv if item.produto.cmv != None else 0
            mov['tipo'] = 'NF_S'
            mov['chave'] = entrega.id        
            m = apps.get_model('estoque.Movimento')
            m.objects.movimento_save(mov)

            '''
            pnf_icms = Pre_nota_ICMS()
            pnf_icms.pre_nota_produtos = pnf_prod
            pnf_icms.aliquota = item.aliq_ICMS
            pnf_icms.codigo_cfop = item.codigo_cfop
            pnf_icms.situacao_tributaria = entrega.operacao.situacao_tributaria
            pnf_icms.aliquota_importacao = ''
            pnf_icms.industria = ''
            pnf_icms.majoracao = ''
            pnf_icms.aliquota_credito = 0
            pnf_icms.save()
            #pnf_ipi = Pre_nota_IPI()
            #pnf_ipi.pre_nota_produtos = pnf_prod
            #pnf_ipi.situacao_tributaria = models.CharField(max_length=3, null=True, blank=True)
            #pnf_ipi.codigo_enquadramento = models.CharField(max_length=3, null=True, blank=True)
            #pnf_ipi.aliquota = models.CharField(max_length=4, null=True, blank=True)
            '''

        #Pre_nota_pedido
        if correcao: 
            pnf_pedido = Pre_nota_pedido.objects.filter(pre_nota = pnf).first()
            if pnf_pedido:
                print('Atualizando - Pnf_pedido: ' + str(pnf_pedido.id))
            else:
                pnf_pedido = Pre_nota_pedido()
                print('Criando - Pnf_pedido: ' + str(pnf_pedido.id))
        else:
            pnf_pedido = Pre_nota_pedido()
            print('Criando - Pnf_pedido: ' + str(pnf_pedido.id))

        pnf_pedido.pre_nota = pnf
        pnf_pedido.presenca = 9
        #pnf_pedido.intermediador
        #pnf_pedido.cnpj_intermediador 
        #pnf_pedido.id_intermediador 
        pnf_pedido.modalidade_frete = entrega.tipo_frete
        pnf_pedido.frete = entrega.valor_frete
        pnf_pedido.desconto = 0
        #pnf_pedido.total = pnf.valor_tot
        #pnf_pedido.despesas_acessorias 
        #pnf_pedido.despesas_aduaneiras 
        #pnf_pedido.informacoes_fisco 
        pnf_pedido.informacoes_complementares = entrega.operacao.mensagem_NF
        pnf_pedido.observacoes_contribuinte = entrega.obs_nf
        #pnf_pedido.forma_pagamento = 1 
        #pnf_pedido.desc_pagamento = 15
        #pnf_pedido.tipo_integracao = 2
        #pnf_pedido.valor_pagamento = entrega.valor_total_entrega
        #pnf_pedido.cnpj_credenciadora 
        #pnf_pedido.bandeira 
        #pnf_pedido.autorizacao
        pnf_pedido.save() 

        #Pre_nota_transporte
        if correcao: 
            pnf_transporte = Pre_nota_transporte.objects.filter(pre_nota = pnf).first()
            if pnf_transporte:
                print('Atualizando - Pnf_transporte: ' + str(pnf_transporte.id))
            else:
                pnf_transporte = Pre_nota_transporte()
                print('Criando - Pnf_transporte: ' + str(pnf_transporte.id))
        else:
            pnf_transporte = Pre_nota_transporte()
            print('Criando - Pnf_transporte: ' + str(pnf_transporte.id))

        pnf_transporte.pre_nota = pnf
        pnf_transporte.volume = entrega.volumes
        pnf_transporte.peso_bruto = entrega.peso_bruto
        pnf_transporte.peso_liquido = entrega.peso_liquido
        pnf_transporte.marca = entrega.marca
        pnf_transporte.numeracao = ''
        pnf_transporte.lacres = ''
        if entrega.transportadora:
            pnf_transporte.cnpj = entrega.transportadora.cnpj
            pnf_transporte.razao_social = entrega.transportadora.nome
            pnf_transporte.ie = entrega.transportadora.insc_est
        #pnf_transporte.cpf = 
        #pnf_transporte.nome_completo = models.CharField(max_length=60, blank=True, null=True)
        #pnf_transporte.endereco = models.CharField(max_length=60, blank=True, null=True)
            pnf_transporte.uf = entrega.transportadora.estado
            pnf_transporte.cidade = entrega.transportadora.cidade
            pnf_transporte.cep = entrega.transportadora.cep
        #pnf_transporte.placa = models.CharField(max_length=7, blank=True, null=True)
        #pnf_transporte.uf_veiculo = models.CharField(max_length=2, blank=True, null=True)
        #pnf_transporte.rntc = models.CharField(max_length=14, blank=True, null=True)
        #pnf_transporte.seguro = models.CharField(max_length=14, blank=True, null=True)
        pnf_transporte.save()

        #Pre_nota_fatura
        if correcao: 
            pnf_fatura = Pre_nota_fatura.objects.filter(pre_nota = pnf).first()
            if pnf_fatura:
                print('Atualizando - Pnf_fatura: ' + str(pnf_fatura.id))
            else:
                pnf_fatura = Pre_nota_fatura()
                print('Criando - Pnf_fatura: ' + str(pnf_fatura.id))
        else:
            pnf_fatura = Pre_nota_fatura()
            print('Criando - Pnf_fatura: ' + str(pnf_fatura.id))

        pnf_fatura.pre_nota = pnf
        pnf_fatura.numero = num_nf
        pnf_fatura.valor = entrega.valor_total_entrega
        pnf_fatura.desconto = '0'
        pnf_fatura.valor_liquido = entrega.valor_total_entrega
        pnf_fatura.save()


        parcelas = Entrega_parcelas.objects.filter(entrega=entrega)
        Pre_nota_parcelas.objects.filter(pre_nota=pnf).delete()
        Conta_receber.objects.filter(entrega = entrega).delete()
        for i, parcela in enumerate(parcelas):
            pnf_parcela = Pre_nota_parcelas()
            pnf_parcela.pre_nota = pnf
            pnf_parcela.vencimento = parcela.vencimento.strftime('%Y-%m-%d')
            pnf_parcela.valor = parcela.valor_parcela
            pnf_parcela.save()
            cr = Conta_receber()
            cr.entrega = entrega
            cr.data_emissao = pnf.data_emissao
            cr.parcela_num = str(pnf.num_nf) + str(i)
            cr.vencimento = parcela.vencimento
            cr.valor_parcela = parcela.valor_parcela
            cr.conta_caixa = entrega.operacao.conta_caixa
            cr.save()
            

    print('Nota fiscal pronta para ser gerada')
    if entrega.status != 3:
        print(gera_nfe(pnf.id))

    return HttpResponse('Pre nota criada')

def pre_nota_estorno(request):
    print('cheguei na view')
    if request.method == 'POST':
        print('estorno estoque')
        entrega_id = request.POST.get('entrega_id')
        m = apps.get_model('estoque.Movimento')
        m.objects.estorno_estoque(entrega_id, 'NF_S')
        return HttpResponse('beleza')
    else:
        return False


def label(request):
    id = request.GET.get('id')
    print(id)
    if id:
            
        ent = Entrega.objects.get(id = id)
        nf = ent.num_nf if ent.num_nf else ''
        destinatario = ent.cliente.apelido if ent.cliente.apelido else ''
        volumes = ent.volumes if ent.volumes else 0
        if ent.pedido_origem:
            num_ped = ent.pedido_origem.num if ent.pedido_origem.num else ''
            num_oc = ent.pedido_origem.num_oc_cli if ent.pedido_origem.num_oc_cli else ''
        else:
            num_ped = ''
            num_oc =''

        lbl_width = 100
        lbl_height = 50
        emissor = 'DEFER INDUSTRIA METALURGICA'
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="Relatorio.pdf"'
        buffer = BytesIO()
        
        print('volumes: ', volumes)
       
        meuKwarg = {}
        meuKwarg['width'] = lbl_width
        meuKwarg['height'] = lbl_height
        meuKwarg['destinatario'] = destinatario
        meuKwarg['nf'] = nf
        meuKwarg['volumes'] = int(volumes) 
        meuKwarg['emissor'] = emissor
        meuKwarg['num_ped'] = num_ped
        meuKwarg['num_oc'] = num_oc
        print('flag 2')

        rep = Label_volumes(buffer, **meuKwarg)
        #pdf = rep.generateReport()
        response.write(rep.show())
    else:
        response = "erro"
    
    return response