from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django_tables2 import SingleTableView
from django_tables2   import RequestConfig
from .models import Prod, Produto
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


@login_required()
def prod_sinc_cyber(request):
    template_name = 'prod/prod_list.html'
     
    ###
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute("""
                select
                    CODIGO,
                    DESCRICAO,
                    COMPLEMENTO_DESC,
                    GRUPO,
                    UNIDADE_MEDIDA,
                    PESO_MERCADORIA,
                    CLASSIFICACAO_FISCAL,
                    ESTOQUE_MINIMO,
                    ESTOQUE_MAXIMO,
                    PCO_VENDA,
                    PCO_CUSTO,
                    ESTOQUE,
                    DATA_INCLUSAO,
                    DATA_MODIFICACAO
                from ACEC1101 
                where grupo = '33'
                """)
    n=0
    cyberprod=[]
    for c in cur.fetchall():
        '''
        d={}
        n = n + 1
        d['num'] = str(n)
        d['cod'] = c[0] + ' - '
        d['descricao'] = c[1]
        cyberprod.append(d)
        '''
        pr = Prod()
        pr.cod = c[0]
        pr.desc = c[1]
        pr.compl = c[2]
        pr.grupoCyber = c[3]
        pr.unidCyber = c[4]
        pr.pLiq = c[5]
        pr.ncmCyber = c[6]
        pr.qEstMin = c[7]
        pr.qEstMax = c[8]
        pr.prVenda =c[9]
        pr.prCusto = c[10]
        pr.qEstoque = c[11]
        pr.save()
        
    conn.close()
    
    data = SincTable(cyberprod)
    print(request.user)
    
    context = {'table': data}
    return render(request, template_name, context)