#from django.contrib.auth.models import User
#from django.forms.formsets import formset_factory
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
#from django_tables2 import SingleTableView
#from django_tables2   import RequestConfig
from .models import *
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
from prod.models import Produto
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

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
    table.paginate(page=request.GET.get("page", 1), per_page=25)
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

def pedido_new(request):
    if request.method == "POST":
        form = PedidoDetailForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('is valid')
            ped = form.save(commit=False)
            ped.save()
            #return render(request, 'comercial/pedido_detail_full.html', {'form': form})
            return redirect('comercial:pedido_full', ped.id) 
        else:
            return render(request, 'comercial/pedido_detail_full.html', {'form': form})     
    else:
        print(request)
        form = PedidoDetailForm()
        return render(request, 'comercial/pedido_detail_full.html', {'form': form})


def pedidos_prod_search(request):
    data = dict()
    #form = PedidoDetailForm(request.POST)
    
    if request.method == 'GET':
        pesq = request.GET.get('pesquisa')
        prod = Prod.objects.only('id', 'cod', 'desc').filter(desc__istartswith = pesq)
        data['table'] = render_to_string(
            'comercial/_prod_table.html',   
            {'prods': prod},
            #request=request
        )
        #return render(request, 'comercial/prod_search2.html', {'tabela': data['table']})
        print('Pesquisa: ' + pesq)
        return HttpResponse(data['table'])
        return HttpResponse('oi')
    else:
        print('Prod search - ' + request.POST)
        return render(request, 'comercial/prod_search2.html' )


def pedidos_prod_search3(request):
    if request.method == 'GET':
        produto = request.GET.get('produto')
        pedido = request.GET.get('pedido')
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
            #request=request
        )
        return JsonResponse(data)


def pedido_item_delete(request):
    pedido_item = request.GET.get('item_id')
    it = Pedido_item.objects.get(pk=pedido_item)
    it.delete()
    return HttpResponse('Produto excluido')

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
        'saldo':l.saldo
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
                #return redirect('comercial:pedido_full', pedido.id)
            #if itens_formset.is_valid():
                for it in formset:
                    if id:
                        new_qtd = it.cleaned_data.get('qtd')
                        item_id = it.cleaned_data.get('item_id')
                        codigo = item_id
                        print(item_id)
                        print(it.cleaned_data)
                        if item_id:
                            #print('ProdComp id: ' + str(item_id))
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