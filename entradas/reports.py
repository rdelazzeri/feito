from django.utils.safestring import mark_safe, SafeData
from .models import *
from core.relatorio_txt import *


def rpt_oc_txt(id):
    print(f'imprimindo oc: {id}' )

    oc = Ordem_compra.objects.get(id=id)
    oc_it = Ordem_compra_itens.objects.filter(ordem_compra = id).select_related()
    r = MeuReport2()

    tipo_oc = oc.status
    r.sub_head('Ordem de compra', 125)
    r.linha(r.campo('Número OC: ', 15, 'l') +  r.campo(oc.num, 20, 'l') +  r.campo('Data emissão: ', 15, 'l') + r.campo(oc.data_emissao, 4, 'l'))
    
    r.sub_head('ITENS', 125)
    r.linha(r.campo('Código', 15, 'l')
                + r.campo('Descrição', 60, 'l')
                + r.campo('Qtd.', 10, 'l')
                + r.campo('Unid.', 8, 'l')
                + r.campo('Pr Unit.', 12, 'l')
                + r.campo('Total', 12, 'l')
                )
      
    for n in oc_it:
        if n:
            linha = (r.campo(n.produto.cod, 15, 'l') 
                        + r.campo(n.produto.desc, 60, 'l') 
                        + r.campo(n.qtd, 10, 'l')
                        + r.campo(n.produto.unid, 8, 'l')
                        + r.campo(n.preco_unit, 12, 'l')
                        + r.campo(n.preco_tot, 12, 'l')
                        )
            r.linha(linha)

    r.sub_head('TOTAIS', 125)
    r.linha(r.campo('Valor total dos produtos: ', 40, 'l') + r.campo(oc.valor_total_produtos, 60, 'l'))     
    r.linha(r.campo('Valor do frete:', 40, 'l') + r.campo(oc.valor_frete, 60, 'l'))  
    r.linha(r.campo('Valor outras despesas: ', 15, 'l') + r.campo(oc.valor_outras_desp, 60, 'l'))  
    r.linha(r.campo('Valor total da OC: ', 15, 'l') + r.campo(oc. valor_total_oc, 60, 'l'))  
 
    return r.rel()


def rpt_oc_linha(id):
    print(f'imprimindo rpt_oc_linha: {id}' )

    oc = Ordem_compra.objects.get(id=id)
    oc_it = Ordem_compra_itens.objects.filter(ordem_compra = id).select_related()
    r = MeuReport2()

    tipo_oc = oc.status
    r.sub_head('Ordem de compra', 125)
    r.linha(r.campo('Número OC: ', 15, 'l') +  r.campo(oc.num, 20, 'l') +  r.campo('Data emissão: ', 15, 'l') + r.campo(oc.data_emissao, 4, 'l'))
    
    r.sub_head('ITENS', 125)
    r.linha(r.campo('Código', 15, 'l')
                + r.campo('Descrição', 60, 'l')
                + r.campo('Qtd.', 10, 'l')
                + r.campo('Unid.', 8, 'l')
                + r.campo('Pr Unit.', 12, 'l')
                + r.campo('Total', 12, 'l')
                )
      
    for n in oc_it:
        if n:
            linha = (r.campo(n.produto.cod, 15, 'l') 
                        + r.campo(n.produto.desc, 60, 'l') 
                        + r.campo(n.qtd, 10, 'l')
                        + r.campo(n.produto.unid, 8, 'l')
                        + r.campo(str(n.preco_unit), 12, 'l')
                        + r.campo(str(n.preco_tot), 12, 'l')
                        )
            r.linha(linha)

    r.sub_head('TOTAIS', 125)
    r.linha(r.campo('Valor total dos produtos: ', 40, 'l') + r.campo(oc.valor_total_produtos, 60, 'l'))     
    r.linha(r.campo('Valor do frete:', 40, 'l') + r.campo(oc.valor_frete, 60, 'l'))  
    r.linha(r.campo('Valor outras despesas: ', 40, 'l') + r.campo(oc.valor_outras_desp, 60, 'l'))  
    r.linha(r.campo('Valor total da OC: ', 40, 'l') + r.campo(oc. valor_total_oc, 60, 'l'))  
 
    return r.rel()

