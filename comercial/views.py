#from django.contrib.auth.models import User
#from django.forms.formsets import formset_factory
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
        return render(request, 'comercial/pedido_detail.html', {'form': form})

class Pedido_read(BSModalReadView):
    model = Pedido
    template_name = 'comercial/pedido_read.html'

def pedido_new(request):
    if request.method == "POST":
        form = PedidoDetailForm(request.POST)
        if form.is_valid():
            ped = form.save(commit=False)
            ped.save()
            return redirect('comercial:pedidos_list')       
    else:
        form = PedidoDetailForm()
        return render(request, 'comercial/pedido_detail.html', {'form': form})