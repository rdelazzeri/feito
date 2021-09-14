from django.shortcuts import render
from django_tables2 import SingleTableView
from django_tables2   import RequestConfig
from .models import Produto
from .tables import SincTable
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
     
    ###
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute("select codigo, descricao from ACEC1101 where grupo = '33'")
    
    n=0
    cyberprod=[]
    for c in cur.fetchall():
        d={}
        n = n + 1
        d['num'] = str(n)
        d['cod'] = c[0] + ' - '
        d['descricao'] = c[1]
        cyberprod.append(d)
    conn.close()
    
    data = SincTable(cyberprod)
    
    context = {'table': data}
    return render(request, template_name, context)