from django.shortcuts import render
from .models import *

def estoque_list(request):
    mov = Movimento.objects.all().order_by('-id')
    #table = PedidosTable(orc)
    #table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, 'estoque/estoque_list.html', {'lista': mov})
