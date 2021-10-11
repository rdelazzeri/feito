from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django_tables2 import SingleTableView
from django_tables2   import RequestConfig
from .models import Prod, Produto, Grupo, Unid, NCM
from .tables import SincTable
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction
from django.forms import modelformset_factory, inlineformset_factory


def prodcomp(request, produto_id):
    produto = Prod.objects.get(pk=produto_id)
    #componentesFormSet = modelformset_factory(ProdComp, fields=('codComp', 'qtd',))
    componentesFormSet = inlineformset_factory(Prod, ProdComp, fk_name='codProd', fields=('codComp', 'qtd',))
    
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
    template_name = 'prod/prod_list.html'
    objects = Produto.objects.all()
    search = request.GET.get('search')
    if search:
        objects = objects.filter(produto__icontains=search)
    context = {'object_list': objects}
    return render(request, template_name, context)

