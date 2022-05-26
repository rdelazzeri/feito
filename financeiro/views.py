from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import CP_Filter


from .models import Conta_pagar

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
    pass


def cr_list(request):
    pass