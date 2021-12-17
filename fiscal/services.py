from .models import *
from cadastro.models import *
from prod.models import *
from comercial.models import *
from django.core import serializers
import json
from core.services import *


def nfe_append(dict, campo, valor):
    if valor:
        dict[campo] = str(valor)
    return dict    


def gera_nfe(prenota_id):

    nfe = {}
    pnf = Pre_nota.objects.get(pk=prenota_id)
    nfe["id"] = pnf.num_nf
    nfe["operacao"] = pnf.operacao
    nfe["natureza_operacao"] = pnf.natureza_operacao
    nfe["modelo"] = pnf.modelo
    nfe["finalidade"] = pnf.finalidade
    nfe["ambiente"] =  pnf.ambiente
    nfe["url_notificacao"] = pnf.url_notificacao

    cli = {}
    nfe_append(cli, "cpf", pnf.cliente.cpf)
    nfe_append(cli, "cpf",pnf.cliente.cpf)
    nfe_append(cli, "nome_completo",pnf.cliente.nome_completo)
    nfe_append(cli, "cnpj",pnf.cliente.cnpj)
    nfe_append(cli, "razao_social",pnf.cliente.razao_social)
    nfe_append(cli, "ie",pnf.cliente.ie)
    nfe_append(cli, "suframa",pnf.cliente.suframa)
    nfe_append(cli, "substituto_tributario","")
    nfe_append(cli, "consumidor_final","")
    nfe_append(cli, "contribuinte","")
    nfe_append(cli, "microcervejaria","")
    nfe_append(cli, "endereco",pnf.cliente.endereco)
    nfe_append(cli, "complemento",pnf.cliente.complemento)
    nfe_append(cli, "numero",pnf.cliente.numero)
    nfe_append(cli, "bairro",pnf.cliente.bairro)
    nfe_append(cli, "cidade",pnf.cliente.cidade)
    nfe_append(cli, "uf",pnf.cliente.uf)
    nfe_append(cli, "cep",pnf.cliente.cep)
    nfe_append(cli, "telefone",pnf.cliente.telefone)
    nfe_append(cli, "email",pnf.cliente.email)
    nfe["cliente"] = cli

    prod = []
    for p in pnf.produtos.all():
        pr  = {}
        nfe_append(pr, "produto_id",p.produto_id) 
        nfe_append(pr, "item",p.item) 
        nfe_append(pr, "nome",p.nome) 
        nfe_append(pr, "codigo",p.codigo)
        nfe_append(pr, "ncm",p.ncm) 
        nfe_append(pr, "quantidade",p.quantidade) 
        nfe_append(pr, "quantidade_tributavel",p.quantidade_tributavel) 
        nfe_append(pr, "unidade",p.unidade)
        nfe_append(pr, "unidade_tributavel",p.unidade_tributavel) 
        nfe_append(pr, "peso",p.peso) 
        nfe_append(pr, "origem",p.origem) 
        nfe_append(pr, "desconto",p.desconto) 
        nfe_append(pr, "subtotal",p.subtotal) 
        nfe_append(pr, "subtotal_tributavel",p.subtotal_tributavel) 
        nfe_append(pr, "total",p.total) 
        nfe_append(pr, "classe_imposto",p.classe_imposto) 
        nfe_append(pr, "cest",p.cest) 
        nfe_append(pr, "beneficio_fiscal",p.beneficio_fiscal) 
        nfe_append(pr, "informacoes_adicionais",p.informacoes_adicionais) 
        nfe_append(pr, "gtin",p.gtin) 
        nfe_append(pr, "gtin_tributavel",p.gtin_tributavel) 
        nfe_append(pr, "cod_barras",p.cod_barras) 
        nfe_append(pr, "cod_barras_tributavel",p.cod_barras_tributavel) 
        nfe_append(pr, "nve",p.nve) 
        nfe_append(pr, "nrecopi",p.nrecopi) 
        nfe_append(pr, "ativo_permanente",p.ativo_permanente) 
        nfe_append(pr, "veiculo_usado",p.veiculo_usado)
        nfe_append(pr, "ex_ipi",p.ex_ipi)
        
        impostos = {}
        if p.icms:
            icms = {}
            nfe_append(icms, "aliquota", p.icms.aliquota)
            nfe_append(icms, "codigo_cfop", p.icms.codigo_cfop)
            nfe_append(icms, "situacao_tributaria", p.icms.situacao_tributaria)
            nfe_append(icms, "aliquota_importacao", p.icms.aliquota_importacao)
            nfe_append(icms, "industria", p.icms.industria)
            nfe_append(icms, "majoracao", p.icms.majoracao)
            nfe_append(icms, "aliquota_credito", p.icms.aliquota_credito)
            impostos["icms"] = icms   
        
        if hasattr(p, 'ipi'):
            ipi = {}
            nfe_append(ipi, "situacao_tributaria", p.ipi.situacao_tributaria)
            nfe_append(ipi, "codigo_enquadramento", p.ipi.codigo_enquadramento)
            nfe_append(ipi, "aliquota", p.ipi.aliquota)
            impostos["ipi"] = ipi

        if hasattr(p, 'pis'):
            pis = {}
            nfe.append(pis, "situacao_tributaria", p.pis.situacao_tributaria)
            nfe.append(pis, "aliquota", p.pis.aliquota)
            impostos["pis"] = pis

        if hasattr(p, 'cofins'):
            cofins = {}
            nfe_append(cofins, "situacao_tributaria", p.cofins.situacao_tributaria)
            nfe_append(cofins, "aliquota", p.cofins.aliquota)
            impostos["cofins"] = cofins
        
        pr["impostos"] = impostos
        prod.append(pr)
    if bool(prod):
        nfe["produtos"] = prod 

    if hasattr(pnf, 'pedido'):
        pedido = {}
        nfe_append(pedido, "presenca", pnf.pedido.presenca)
        nfe_append(pedido, "intermediador", pnf.pedido.intermediador)
        nfe_append(pedido, "cnpj_intermediador", pnf.pedido.cnpj_intermediador)
        nfe_append(pedido, "id_intermediador", pnf.pedido.id_intermediador)
        nfe_append(pedido, "modalidade_frete", pnf.pedido.modalidade_frete)
        nfe_append(pedido, "frete", pnf.pedido.frete)
        nfe_append(pedido, "desconto", pnf.pedido.desconto)
        nfe_append(pedido, "total", pnf.pedido.total)
        nfe_append(pedido, "despesas_acessorias", pnf.pedido.despesas_acessorias)
        nfe_append(pedido, "despesas_aduaneiras", pnf.pedido.despesas_aduaneiras)
        nfe_append(pedido, "informacoes_fisco", pnf.pedido.informacoes_fisco)
        nfe_append(pedido, "informacoes_complementares", pnf.pedido.informacoes_complementares)
        nfe_append(pedido, "observacoes_contribuinte", pnf.pedido.observacoes_contribuinte)
        nfe_append(pedido, "pagamento", pnf.pedido.pagamento)
        nfe_append(pedido, "forma_pagamento", pnf.pedido.forma_pagamento)
        nfe_append(pedido, "desc_pagamento", pnf.pedido.desc_pagamento)
        nfe_append(pedido, "tipo_integracao", pnf.pedido.tipo_integracao)
        nfe_append(pedido, "valor_pagamento", pnf.pedido.valor_pagamento)
        nfe_append(pedido, "cnpj_credenciadora", pnf.pedido.cnpj_credenciadora)
        nfe_append(pedido, "bandeira", pnf.pedido.bandeira)
        nfe_append(pedido, "autorizacao", pnf.pedido.autorizacao)
        if bool(pedido):
            nfe["pedido"] = pedido

    if hasattr(pnf, 'transporte'):
        transporte = {}
        nfe_append(transporte, "volume", pnf.transporte.volume)
        nfe_append(transporte, "peso_bruto", pnf.transporte.peso_bruto)
        nfe_append(transporte, "peso_liquido", pnf.transporte.peso_liquido)
        nfe_append(transporte, "marca", pnf.transporte.marca)
        nfe_append(transporte, "numeracao", pnf.transporte.numeracao)
        nfe_append(transporte, "lacres", pnf.transporte.lacres)
        nfe_append(transporte, "cnpj", pnf.transporte.cnpj)
        nfe_append(transporte, "razao_social", pnf.transporte.razao_social)
        nfe_append(transporte, "ie", pnf.transporte.ie)
        nfe_append(transporte, "cpf", pnf.transporte.cpf)
        nfe_append(transporte, "nome_completo", pnf.transporte.nome_completo)
        nfe_append(transporte, "endereco", pnf.transporte.endereco)
        nfe_append(transporte, "uf", pnf.transporte.uf)
        nfe_append(transporte, "cidade", pnf.transporte.cidade)
        nfe_append(transporte, "cep", pnf.transporte.cep)
        nfe_append(transporte, "placa", pnf.transporte.placa)
        nfe_append(transporte, "uf_veiculo", pnf.transporte.uf_veiculo)
        nfe_append(transporte, "rntc", pnf.transporte.rntc)
        nfe_append(transporte, "seguro", pnf.transporte.seguro)

    if hasattr(pnf, 'entrega'):
        entrega = {}
        nfe_append(entrega, "cpf", pnf.entrega.cpf)
        nfe_append(entrega, "nome_completo", pnf.entrega.nome_completo)
        nfe_append(entrega, "cnpj", pnf.entrega.cnpj)
        nfe_append(entrega, "razao_social", pnf.entrega.razao_social)
        nfe_append(entrega, "ie", pnf.entrega.ie)
        nfe_append(entrega, "endereco", pnf.entrega.endereco)
        nfe_append(entrega, "complemento", pnf.entrega.complemento)
        nfe_append(entrega, "numero", pnf.entrega.numero)
        nfe_append(entrega, "bairro", pnf.entrega.bairro)
        nfe_append(entrega, "cidade", pnf.entrega.cidade)
        nfe_append(entrega, "uf", pnf.entrega.uf)
        nfe_append(entrega, "cep", pnf.entrega.cep)
        nfe_append(entrega, "telefone", pnf.entrega.telefone)
        nfe_append(entrega, "email", pnf.entrega.email)
        if bool(entrega):
            nfe["transporte"] = entrega
    
    if bool(transporte):
           nfe["transporte"] = transporte


    if hasattr(pnf, 'fatura'):
        fatura = {}
        nfe_append(fatura, "numero", pnf.fatura.numero)
        nfe_append(fatura, "valor", pnf.fatura.valor)
        nfe_append(fatura, "desconto", pnf.fatura.desconto)
        nfe_append(fatura, "valor_liquido", pnf.fatura.valor_liquido)
        if bool(fatura):
            nfe["fatura"] = fatura


    parcelas = []
    for p in pnf.parcelas.all():
        parcela  = {}
        nfe_append(parcela, "vencimento", p.vencimento)
        nfe_append(parcela, "valor", p.valor)
        if bool(parcela):
            parcelas["parcelas"] = parcela
    if bool(parcelas):
        nfe["parcelas"] = parcelas

    return nfe


