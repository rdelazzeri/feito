from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django_tables2 import SingleTableView
from django_tables2   import RequestConfig
from .models import Prod, Produto, Grupo, Unid, NCM
from .tables import SincTable, ProdTable
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

'''
def prod_list(request):
    template_name = 'prod/search_prod.html'
    objects = Prod.objects.all()
    search = request.GET.get('search')
    if search:
        pass
        #objects = objects.filter(produto__icontains=search)
    context = {'object_list': objects}
    return render(request, template_name, context)

'''
def prod_list(request):
    filter = ProdFilter(request.GET, queryset=Prod.objects.all())
    return render(request, 'prod/search_prod.html', {'filter': filter})

'''
class prod_list(SingleTableMixin, FilterView):
    table_class = ProdTable
    model = Prod
    template_name = "prod_list.html"

    filterset_class = ProdFilter
'''