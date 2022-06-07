from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import CP_Filter
from .forms import CP_detail_form
from .models import Conta_pagar
from cadastro.models import Parceiro
from entradas.models import NF_entrada
from dal import autocomplete



class ParcAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print('nome-autocomplete')
        if not self.request.user.is_authenticated:
            return Parceiro.objects.none()
        qs = Parceiro.objects.only('nome')
        if self.q:
            qs = qs.filter(nome__icontains=self.q)
        return qs
        
class EntradaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print('nome-autocomplete')
        if not self.request.user.is_authenticated:
            return NF_entrada.objects.none()
        qs = NF_entrada.objects.only('num', 'parceiro')
        if self.q:
            qs = qs.filter(parceiro__nome__icontains=self.q)
        return qs


def cp_list(request):
    lista = CP_Filter(request.GET, queryset=Conta_pagar.objects.all().order_by('-data_vencimento'))
    paginator = Paginator(lista.qs, 20) # Show 25 contacts per page.
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'financeiro/cp_list.html', {'page_obj': page_obj, 'lista': lista})

def cp_detail(request, pk):
    cp = get_object_or_404(Conta_pagar, pk=pk)
    if request.method == 'POST':
        #print(request.POST)
        act = request.POST['act']

        if act == 'delete':
            cp.delete()
            form = CP_detail_form()
            return redirect('financeiro:cp_list')
        elif act == 'save':
            print('act=save')
            #pr = get_object_or_404(Prod, pk=prod_id)
            form = CP_detail_form(request.POST, instance = cp)
            if form.is_valid():
                print('form is valid')
                #form = ProdDetailForm(form.cleaned_data)
                form.save()
            return render(request, 'financeiro/cp_detail.html', {'form': form})
        elif act =='quitar':
            return redirect('prod:prod_comp', pk)
    else:
        form = CP_detail_form(instance=cp)
        return render(request, 'financeiro/cp_detail.html', {'form': form, 'cp_id':pk})


def cp_new(request):
    if request.method == 'POST':
        form = CP_detail_form(request.POST)
        if form.is_valid():
            cp = form.save(commit=False)
            cp.save()
            return redirect('financeiro:cp_detail', pk=cp.pk)
        else:
            return render(request, 'prod/prod_detail.html', {'form': form})
    else:
        form = CP_detail_form()
        return render(request, 'financeiro/cp_detail.html', {'form': form})


def cr_list(request):
    pass