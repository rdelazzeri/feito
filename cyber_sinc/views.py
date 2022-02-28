from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from prod.models import Prod, Prod, Grupo, Unid, NCM, ProdComp
from cadastro.models import Parceiro, Tipo_parceiro
import firebirdsql


@login_required()
def cyber_sinc(request):
    template_name = 'cyber_sinc/cyber_sinc.html'    
    context = {'context': ''}
    return render(request, template_name, context)

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
            ['M', 'Metro'],
            ['NC', 'Não Cadastrado'],
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
    nc = NCM()
    nc.cod = '0'
    nc.desc = 'Não Cadastrado'
    nc.save()

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


@login_required()
def cyber_sinc_composicao(request):
    template_name = 'cyber_sinc/cyber_sinc.html'
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute('select prcodigo, cmcodigo, cmquantidade, ugmodificadoreg, uginseridoreg from agpc03cm')
    
    ProdComp.objects.all().delete()

    for c in cur.fetchall():
        
        try:
            prodprod = Prod.objects.get(cod = c[0])
        except:
            prodprod = Prod.objects.get(cod = '999')
        
        try:
            prodcomp = Prod.objects.get(cod = c[1])
        except:
            prodcomp = Prod.objects.get(cod = '999')

        pr = ProdComp()
        pr.codProd = prodprod
        pr.codComp = prodcomp
        pr.qtd = c[2]
        pr.save()
        
    conn.close()
    
    context = {'context': 'composição feito'}
    return render(request, template_name, context)

    
@login_required()
def cyber_sinc_pessoa(request):
    template_name = 'cyber_sinc/cyber_sinc.html'
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute("""
            select
                OBSERVACAO,
                PESSOA_FISICAOUJURIDICA,
                NOME,
                NOME_FANTASIA,
                CGC_CNPJ,
                CLIE,
                CLENDERECO,
                CLENDNUMERO,
                CLENDCOMPLEMENTO,
                BAIRRO,
                CIDADE,
                ESTADO,
                TELEFONE1,
                TELEFONE2
            FROM augc0301
            ORDER BY NOME
                """)
    #Prod.objects.all().delete()
    Parceiro.objects.all().delete()

    tipo_parc = Tipo_parceiro.objects.get(sigla='C')
    print('Tipo de parceiro cliente selecionado: ' + str(tipo_parc))

    for c in cur.fetchall():
        parc = Parceiro()
        parc.obs = c[0]
        parc.pessoa = c[1]
        parc.nome = c[2]
        parc.apelido = c[3]
        if c[1] == 'J':
            parc.cnpj = c[4]
            parc.insc_est = c[5]
        elif c[1] == 'F':
            parc.cpf = c[4]
        parc.logradouro = c[6]
        parc.numero = c[7]
        parc.complemento = c[8]
        parc.bairro = c[9]
        parc.cidade = c[10]
        parc.estado = c[11]
        parc.fone1 = c[12]
        parc.fone2 = c[13]
        parc.save()
        parc.tipo.add(tipo_parc)


    print('clientes ok')
## importação de fornecedores

    cur.execute("""
            select
                FOBS,
                FJUR_FIS,
                FNOME,
                FNOME_FANTASIA,
                FCNPJ_CIC,
                FIE,
                FOENDERECO,
                FOENDNUMERO,
                FOENDCOMPLEMENTO,
                FBAIRRO,
                FCIDADE,
                FUF,
                FFONE1,
                FFONE2,
                FOBS2,
                FTIPO
            FROM augc0501
            ORDER BY FNOME
                """)
    #Prod.objects.all().delete()
    #Parceiro.objects.all().delete()

    for c in cur.fetchall():

        try:
            parc = Parceiro.objects.get(nome = c[2])
            parc.obs = str(parc.obs) + str(c[0])
            parc.tipo.add(Tipo_parceiro.objects.get(sigla='F'))
            if c[15] != 'F':
                try:
                    parc.tipo.add(Tipo_parceiro.objects.get(sigla = c[15]))
                except:
                    pass
        except:
            parc = Parceiro()
            parc.obs = c[0]
            parc.pessoa = c[1]
            parc.nome = c[2]
            parc.apelido = c[3]
            if c[1] == 'J':
                parc.cnpj = c[4]
                parc.insc_est = c[5]
            elif c[1] == 'F':
                parc.cpf = c[4]
            parc.logradouro = c[6]
            parc.numero = c[7]
            parc.complemento = c[8]
            parc.bairro = c[9]
            parc.cidade = c[10]
            parc.estado = c[11]
            parc.fone1 = c[12]
            parc.fone2 = c[13]
            parc.email_contato = c[14]
            parc.save()
            #print('nome: ' + str(c[2]) + ' estado: ' + str(c[10]) )
            parc.tipo.add(Tipo_parceiro.objects.get(sigla='F'))
            if c[15] != 'F':
                try:
                    parc.tipo.add(Tipo_parceiro.objects.get(sigla = c[15]))
                except:
                    pass
    conn.close()

    context = {'context': 'Clientes feito'}
    return render(request, template_name, context)