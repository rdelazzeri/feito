from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django_tables2 import SingleTableView
from django_tables2   import RequestConfig
from .models import Prod, Produto, Grupo, Unid, NCM
from .tables import SincTable
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction

'''
class Prod_Create(CreateView):
    model = Prod
    template_name = 'prod/prod_create.html'
    form_class = ProdForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(Prod_Create, self).get_context_data(**kwargs)
        if self.request.POST:
            data['codComp'] = ProdCompFormSet(self.request.POST)
        else:
            data['codComp'] = ProdCompFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        Comp = context['codComp']
        with transaction.atomic():
            form.instance.criadoPor = self.request.user
            self.object = form.save()
            if Comp.is_valid():
                Comp.instance = self.object
                Comp.save()
        return super(Prod_Create, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Prod:prod_detail', kwargs={'pk': self.object.pk})

class Prod_Update(CreateView):
    model = Prod
    template_name = 'prod/prod_create.html'
    form_class = ProdForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(Prod_Update, self).get_context_data(**kwargs)
        if self.request.POST:
            data['codComp'] = ProdCompFormSet(self.request.POST, instance=self.object)
        else:
            data['codComp'] = ProdCompFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        Comp = context['codComp']
        with transaction.atomic():
            form.instance.criadoPor = self.request.user
            self.object = form.save()
            if Comp.is_valid():
                Comp.instance = self.object
                Comp.save()
        return super(Prod_Create, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Prod:prod_detail', kwargs={'pk': self.object.pk})


'''






def prod_list(request):
    template_name = 'prod/prod_list.html'
    objects = Produto.objects.all()
    search = request.GET.get('search')
    if search:
        objects = objects.filter(produto__icontains=search)
    context = {'object_list': objects}
    return render(request, template_name, context)

