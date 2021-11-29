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
#from django.urls import reverse_lazy
#from django.db import transaction
#from django.forms import modelformset_factory, inlineformset_factory, formset_factory
#from django_filters.views import FilterView
#from django_tables2.views import SingleTableMixin

  
def pedidos_new(request):
    if request.method == "POST":
        form = PedidoDetailForm(request.POST)
        if form.is_valid():
            ped = form.save(commit=False)
            ped.save()
            return redirect('comercial:pedidos_list')       
    else:
        form = PedidoDetailForm()
        return render(request, 'comercial/pedido_detail.html', {'form': form})

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

def pedidos_list(request):
    ped = Pedido.objects.all()
    table = PedidosTable(ped)
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, 'comercial/pedidos_list.html', {'table': table})


