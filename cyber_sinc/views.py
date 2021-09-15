from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from prod.models import Prod, Produto, Grupo, Unid, NCM
import firebirdsql


@login_required()
def cyber_sinc_grupos(request):
    template_name = 'cyber_sinc/cyber_sinc.html'
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute("""
                select
                    CODIGO,
                    DESCRICAO
                from acec1201
                """)
    
    Grupo.objects.all().delete()

    for c in cur.fetchall():
        pr = Grupo()
        pr.cod = c[1][0:4]
        pr.desc = c[1][7:]
        pr.cod_cyber = c[0]
        pr.save()
        
    conn.close()
    
    context = {'context': 'grupos feito'}
    return render(request, template_name, context)

@login_required()
def cyber_sinc_unid(request):
    template_name = 'cyber_sinc/cyber_sinc.html'
    
    UNIDS = [
            ['PC' , 'Peça'],
            ['MT' , 'Metro'],
            ['BD' , 'Balde'],
            ['FD' , 'Fardo'],
            ['GL' , 'Galão'],
            ['GR' , 'Gramas'],
            ['M2' , 'Metro Quadrado'],
            ['CX' , 'Caixa'],
            ['CT' , 'Cento'],
            ['M3' , 'Metro Cúbico'],
            ['MI' , 'Milheiro'],
            ['BB' , 'Bombona'],
            ['LT' , 'Litro'],
            ['PCT' , 'Pacote'],
            ['KW' , 'Kilowatt'],
            ['UN' , 'Unidade'],
            ['KG' , 'Quilograma'],
            ['TON' , 'Tonelada'],
    ]
        
    Unid.objects.all().delete()

    for unid in UNIDS:
        u = Unid()
        u.unid = unid[0]
        u.desc = unid[1]
        u.save()

    context = {'context': 'Unid feito'}
    return render(request, template_name, context)


@login_required()
def cyber_sinc_ncm(request):
    template_name = 'cyber_sinc/cyber_sinc.html'
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute("""
                select
                    NCCODIGO,
                    NCDESCRICAO
                from acec15nc
                """)
    #Prod.objects.all().delete()
    NCM.objects.all().delete()

    for c in cur.fetchall():
        nc = NCM()
        nc.cod = c[0]
        nc.desc = c[1]
        nc.save()
        
    conn.close()
    
    context = {'context': 'NCM feito'}
    return render(request, template_name, context)



@login_required()
def prod_sinc_cyber(request):
    template_name = 'cyber_sinc/cyber_sinc.html'
    
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
                """)
                #where grupo = '33'

    Prod.objects.all().delete()

    for c in cur.fetchall():
       
        gr = Grupo.objects.get(cod_cyber = c[3])
        #print(gr.cod)
        try:
            unid = Unid.objects.get(unid = c[4])
        except:
            unid = Unid.objects.get(unid = 'NC')
        
        try:
            ncm = NCM.objects.get(cod = c[6])
        except:
            ncm = NCM.objects.get(cod = '0')
            

        #print(ncm.cod)

        pr = Prod()
        pr.cod = c[0]
        pr.desc = c[1]
        pr.compl = c[2]
        pr.grupo = gr
        pr.grupoCyber = int(c[3])
        pr.unidCyber = c[4]
        pr.unid = unid
        pr.pLiq = c[5]
        pr.ncm = ncm
        pr.NCMCyber = c[6]
        pr.qEstMin = c[7]
        pr.qEstMax = c[8]
        pr.prVenda =c[9]
        pr.prCusto = c[10]
        pr.qEstoque = c[11]
        pr.save()
        
    conn.close()
    

    print(request.user)
    
    context = {'context': 'Produtos feito' }
    return render(request, template_name, context)