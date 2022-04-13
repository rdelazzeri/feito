from asyncio.windows_events import NULL
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from prod.models import Prod, Prod, Grupo, Unid, NCM, ProdComp
from cadastro.models import Parceiro, Tipo_parceiro
from entradas.models import NF_entrada, NF_entrada_itens, Operacao_entrada
from comercial.models import Entrega, Entrega_item, Operacao, Pedido, Pedido_item
from financeiro.models import Plano_contas
import firebirdsql
from django.utils.dateparse import parse_date

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
    
    #Grupo.objects.all().delete()

    for c in cur.fetchall():
        cyber_cod = c[1][0:4]
        try:
            pr = Grupo.objects.get(cod = cyber_cod)
        except:
            pr = Grupo()
        pr.cod = cyber_cod
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
    #NCM.objects.all().delete()

    for c in cur.fetchall():
        try:
            nc = NCM.objects.get(cod = c[0])
        except:
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

    #Prod.objects.all().delete()

    for c in cur.fetchall():
       
        try:
            gr = Grupo.objects.filter(cod_cyber = c[3])[0]
        except:
            gr = Grupo.objects.filter(cod_cyber = '999')[0]
        
        try:
            unid = Unid.objects.get(unid = c[4])
        except:
            unid = Unid.objects.get(unid = 'NC')
        
        try:
            ncm = NCM.objects.filter(cod = c[6])[0]
        except:
            ncm = NCM.objects.filter(cod = '0')[0]
            
        try:
            pr = Prod.objects.get(cod = c[0])
        except:
            pr = Prod()
        #print(ncm.cod)
        
        pr.cod = c[0]
        pr.desc = c[1]
        pr.compl = c[2]
        pr.grupo = gr
        pr.grupoCyber = int(c[3]) if c[3] else 0
        pr.unidCyber = c[4]
        pr.unid = unid
        pr.fatorUnid = c[5]
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
                TELEFONE2,
                CEP
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
        parc.cep = c[14]
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
                FTIPO,
                CEP
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
            parc.cep = c[16]
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




##-----------------------notas




#Operacao
def cyber_sinc_operacao(request):
    template_name = 'cyber_sinc/cyber_sinc.html'
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute("""
                select
                    CONTA,
                    DESCRICAO,
                    CONTA_DE_BANCO,
                    SENHA
                from ACXC9001
                """)
    
    NF_entrada.objects.all().delete()
    Operacao_entrada.objects.all().delete()
    Plano_contas.objects.exclude(num = '1').delete()
    

    for c in cur.fetchall():
        pl = Plano_contas()
        pl.desc = c[1]
        pl.num = c[0]
        pl.cod_cyber = c[0]
        pl.banco = c[2]
        pl.nivel = c[3]
        pl.save()

        op = Operacao_entrada()
        op.desc = c[1]
        op.conta_caixa = pl
        op.conta_credito = pl
        op.conta_debito = pl
        op.save()
        
    conn.close()
    
    context = {'context': 'plano de contas feito'}
    return render(request, template_name, context)


#nota master
def cyber_sinc_nf_e(request):
    template_name = 'cyber_sinc/cyber_sinc.html'

    NF_entrada.objects.all().delete()

    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute("""
            select

                    DOCUMENTO,                                     
                    COD_CLI,               
                    SERIE_DOC,             
                    OPERACAO_DOC,              
                    DATA,              
                    TOTAL_DOC,             
                    ICMS_DOC,              
                    TRANSPORTADORA,            
                    BCI,               
                    OBSERVACAO_NF,             
                    DESCONTO_GERAL,             
                    DESPESAS,               
                    FRETE,              
                    TOTAL_ICMS,             
                    VALOR_SEGURO,               
                    TOTAL_PRODUTOS,             
                    TOTAL_IPI,              
                    FRETE1_2,               
                    B.COD_NATUREZA,             
                    B.XCCODIGO,        
                    COD_OP,
                    C.FCNPJ_CIC

                from acem1401
                JOIN afvc0901 B ON (OPERACAO_DOC = COD_OP)
                JOIN AUGC0501 C ON (COD_CLI = C.FCOD)
                where data > '2011-01-01'
                        AND ENTRADA_SAIDA = 'E'
                """)

    #for c in cur.fetchall():
    c =  cur.fetchone()
    while c:
        print(c[21])
        cnpj1 = str(c[21])
        cnpj2 = cnpj1.replace('.', '')
        cnpj2 = cnpj2.replace('-', '')
        cnpj2 = cnpj2.replace('/', '')
        print(cnpj2)
        #parc = Parceiro.objects.filter(cnpj = cnpj_limpo)
        parc = Parceiro.objects.filter(cnpj = cnpj2) if Parceiro.objects.filter(cnpj = cnpj2) else Parceiro.objects.filter(cnpj = '04408568000105')
        try:
            ct = Plano_contas.objects.get(num = c[19])
            op = Operacao_entrada.objects.filter(desc = ct.desc) 
        except:
             Plano_contas.objects.get(id = 1)
             op = Operacao_entrada.objects.filter(desc = ct.desc)

        nf = NF_entrada()
        nf.num = c[0]
        nf.parceiro = parc[0]
        nf.serie = c[2]
        nf.conta = ct
        nf.operacao = op[0]
        nf.data_emissao = c[4]
        nf.desconto = c[10]
        nf.valor_frete = c[12]
        nf.valor_seguro = c[14]
        nf.tipo_frete = c[17]
        nf.chave_cyber = c[1]
        nf.save()

        c = cur.fetchone()
        
    conn.close()
    print('nf entrada ok')
    context = {'context': 'Notas de entrada feito'}
    return render(request, template_name, context)


def cyber_sinc_nf_ei(request):
    
    template_name = 'cyber_sinc/cyber_sinc.html'
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()

    NF_entrada_itens.objects.all().delete()

    ## importação de itens das 00notas
    cur.execute("""
            select
                DOCUMENTO,
                COD_CLI,
                CODIGOPRODUTO,
                QUNATIDADEPRODUTO,
                VALOR_UNITARIOPRODUTO,
                ICMS_ITEM,
                IPI_ITEM,
                OBSERVACAO_PRODUTO
            FROM ACEM14IT
            where data > '2011-01-01'
                    AND SERIE = '1'
            
                """)
    #Prod.objects.all().delete()
    #Parceiro.objects.all().delete()

    #for c in cur.fetchall():
    c =  cur.fetchone()
    while c:

        try:
            nf2 = NF_entrada.objects.get(chave_cyber = c[1], num = c[0] )
            nf = nf2
            print(nf.num)
        except:
            nf2 = NF_entrada.objects.all()
            nf = nf2[0]
            print('nf nao localizada')

        try:
            prod = Prod.objects.get(cod = c[2])
        except:
            prod = Prod.objects.get(cod = '999')
        
        nfi = NF_entrada_itens()
        
        nfi.nf_entrada = nf
        nfi.produto = prod
        nfi.qtd = c[3]
        nfi.preco_unit = c[4]
        nfi.aliq_icms = c[5]
        nfi.aliq_ipi = c[6]
        nfi.obs = c[7]
        nfi.save()
        print(nfi.produto.desc)

        
        c = cur.fetchone()

    conn.close()

    context = {'context': 'Itens da nfe entrada feito'}
    return render(request, template_name, context)







####---------------------------------entregas

#Operacao
def cyber_sinc_operacao_saida(request):
    template_name = 'cyber_sinc/cyber_sinc.html'
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute("""
                    select cod_natureza, xccodigo
                    from afvc0901
                    where tipo_op in ('2', '6', '9', 'c', 'd')
                    group by cod_natureza, xccodigo
                """)
    
    #NF_entrada.objects.all().delete()
    #Operacao.objects.all().delete()
    #Plano_contas.objects.exclude(num = '1').delete()
    
    for c in cur.fetchall():
        try:
            pl = Plano_contas.objects.get(num = c[1])
        except:
            pl = None

        op = Operacao()
        op.desc = c[0]
        op.natureza_operacao = c[0]
        op.tipo = '1'
        op.CFOP = c[0]
        op.origem_mercadoria = '0'
        op.conta_caixa = pl
        op.save()
        
    conn.close()
    
    context = {'context': 'plano de contas feito'}
    return render(request, template_name, context)

#nota master
def cyber_sinc_nf_s(request):
    template_name = 'cyber_sinc/cyber_sinc.html'

    Entrega.objects.all().delete()

    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()
    cur.execute("""
            select
                    DOCUMENTO,                                     
                    COD_CLI,               
                    SERIE_DOC,             
                    OPERACAO_DOC,              
                    DATA,              
                    TOTAL_DOC,             
                    ICMS_DOC,              
                    A.TRANSPORTADORA,            
                    BCI,               
                    OBSERVACAO_NF,             
                    DESCONTO_GERAL,             
                    DESPESAS,               
                    FRETE,              
                    TOTAL_ICMS,             
                    VALOR_SEGURO,               
                    TOTAL_PRODUTOS,             
                    TOTAL_IPI,              
                    FRETE1_2,               
                    B.COD_NATUREZA,             
                    B.XCCODIGO,        
                    COD_OP,
                    C.CGC_CNPJ

                from acem1401 A
                JOIN afvc0901 B ON (OPERACAO_DOC = COD_OP)
                JOIN AUGC0301 C ON (COD_CLI = C.CODIGO_CLIENTE)
                where data > '2011-01-01'
                        AND ENTRADA_SAIDA = 'S'
                order by documento
                """)

    #for c in cur.fetchall():
    
    #cadastrar pedido generico
    try:
        ped = Pedido.objects.get(num = 0)
    except:
        ped = Pedido()
        ped.num = 0
        ped.obs = 'Pedido Genérico'
        ped.save()
        prod = Prod.objects.get(cod = '999')
        pedit = Pedido_item()
        pedit.pedido = ped
        pedit.produto = prod
        pedit.save()

    c =  cur.fetchone()
    while c:
        print('NF: %s - CNPJ: %s',(c[0], c[21]))
        doc = c[21]
        if len(doc) > 14:
            cnpj1 = str(c[21])
            cnpj2 = cnpj1.replace('.', '')
            cnpj2 = cnpj2.replace('-', '')
            cnpj2 = cnpj2.replace('/', '')
            #print(cnpj2)
            #parc = Parceiro.objects.filter(cnpj = cnpj_limpo)
            parc = Parceiro.objects.filter(cnpj = cnpj2) if Parceiro.objects.filter(cnpj = cnpj2) else Parceiro.objects.filter(cnpj = '04408568000105')
        else:
            cpf = doc.replace('.', '')
            cpf = doc.replace('-', '')
            #print(cnpj2)
            #parc = Parceiro.objects.filter(cnpj = cnpj_limpo)
            parc = Parceiro.objects.filter(cpf = cpf) if Parceiro.objects.filter(cpf = cpf) else Parceiro.objects.filter(cnpj = '04408568000105')
        try:
            #ct = Plano_contas.objects.get(num = c[19])
            op = Operacao.objects.get(CFOP = c[18]) 
        except:
             op = Operacao.objects.get(CFOP = '05901')

        try:
            nf = Entrega.objects.get(num_nf = c[0])
        except:
            nf = Entrega()

        nf.num = c[0]
        nf.num_nf = c[0]
        nf.cliente = parc[0]
        nf.operacao = op
        nf.pedido_origem = ped
        nf.data_emissao = parse_date(c[4])
        nf.valor_frete = c[12]
        nf.tipo_frete = c[17] if c[17] else '2'
        nf.save()

        c = cur.fetchone()
        
    conn.close()
    print('nf entrada ok')
    context = {'context': 'Notas de saida feito'}
    return render(request, template_name, context)


def cyber_sinc_nf_si(request):
    
    template_name = 'cyber_sinc/cyber_sinc.html'
    conn = firebirdsql.connect(dsn='localhost:/cybersul/banco/dadosadm.fdb', user='sysdba', password='masterkey', charset='ISO8859_1')
    cur = conn.cursor()

    Entrega_item.objects.all().delete()

    ## importação de itens das 00notas
    cur.execute("""
            select
                DOCUMENTO,
                COD_CLI,
                CODIGOPRODUTO,
                QUNATIDADEPRODUTO,
                VALOR_UNITARIOPRODUTO,
                ICMS_ITEM,
                IPI_ITEM,
                OBSERVACAO_PRODUTO
            FROM ACEM14IT
            where data > '2011-01-01'
                    AND SERIE = 'E1'
            
                """)
    #Prod.objects.all().delete()
    #Parceiro.objects.all().delete()

    #for c in cur.fetchall():

    pedit = Pedido_item.objects.filter(pedido__num = 0).first()
    print(pedit)
    c =  cur.fetchone()
    while c:

        try:
            prod = Prod.objects.get(cod = c[2])
        except:
            prod = Prod.objects.get(cod = '999')

        try:
            nf = Entrega.objects.get(num_nf = c[0] )
            print(c[0])
            nfi = Entrega_item()
            nfi.entrega = nf
            nfi.produto = prod
            nfi.pedido_item = pedit
            nfi.qtd = c[3]
            nfi.pr_unit = c[4]
            nfi.aliq_ICMS = c[5]
            nfi.aliq_IPI = c[6]
            nfi.obs = c[7]
            nfi.save()
            print(nfi.produto.desc)
        except:
            print('nf nao localizada: %s',(c[0]) )
        
        c = cur.fetchone()

    conn.close()

    context = {'context': 'Itens da nfe entrada feito'}
    return render(request, template_name, context)
