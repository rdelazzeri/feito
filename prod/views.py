from django.shortcuts import render
from .models import Produto
import firebirdsql


def prod_list(request):
    template_name = 'prod/prod_list.html'
    objects = Produto.objects.all()
    search = request.GET.get('search')
    if search:
        objects = objects.filter(produto__icontains=search)
    context = {'object_list': objects}
    return render(request, template_name, context)



def prod_sinc_cyber(request):
    template_name = 'prod/prod_list.html'
    objects = Produto.objects.all()
    
    cyberprod=[]
    ###
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute("select * from ACEC1101")
    
    n=0
    for c in cur:
        n = n + 1
        cyberprod.append(c[0] + ' - ' + str(n))
    conn.close()

    search = request.GET.get('search')
    if search:
        objects = objects.filter(produto__icontains=search)
    context = {'object_list': cyberprod}
    return render(request, template_name, context)