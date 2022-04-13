from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from pathlib import Path
from django.utils.safestring import mark_safe, SafeData
from .models import *
from core.relatorio_txt import *


def rpt_op_txt(id):
    print(f'imprimindo op: {id}' )

    op = OP.objects.get(id=id)
    op_comp_fis = OP_componente_fisico.objects.filter(op = id).select_related()
    r = MeuReport()

    r.sub_head('ORDEM DE PRODUÇÃO', 125)
    r.linha(r.campo('Número OP: ', 15, 'l') +  r.campo(op.num, 20, 'l') +  r.campo('Data emissão: ', 15, 'l') + r.campo(op.data_emissao, 4, 'l'))
    
    r.sub_head('PRODUTO', 125)
    r.linha(r.campo('Código', 15, 'l')
                + r.campo('Descrição', 60, 'l')
                + r.campo('Qtd.', 10, 'l')
                + r.campo('Unid.', 8, 'l')
                + r.campo('Qtd2', 8, 'l')
                + r.campo('Unid2', 8, 'l')
                )
    r.linha(r.campo(op.produto.cod, 15, 'l')
                + r.campo(op.produto.desc, 60, 'l')
                + r.campo(op.qtd_programada, 10, 'l')
                + r.campo(op.produto.unid, 8, 'l')
                + r.campo(op.produto.fatorUnid, 8, 'l')
                + r.campo(op.produto.unid2, 8, 'l')
                )

    r.sub_head('COMPOSIÇÃO', 125)
    r.linha(r.campo('Código', 15, 'l')
                + r.campo('Descrição', 60, 'l')
                + r.campo('Qtd.', 10, 'l')
                + r.campo('Unid.', 8, 'l')
                + r.campo('Qtd2', 8, 'l')
                + r.campo('Unid2', 8, 'l')
                )           

    for n in op.op_comp_fis.all():
        if n:
            linha = (r.campo(n.produto.cod, 15, 'l') 
                        + r.campo(n.produto.desc, 60, 'l') 
                        + r.campo(n.qtd_programada, 10, 'l'))
            
            linha = linha + r.campo(n.produto.unid, 8, 'l') if n.produto.unid else linha + r.campo('', 8, 'b')
            linha = linha + r.campo(n.produto.fatorUnid, 8, 'l') if n.produto.fatorUnid else linha + r.campo('', 8, 'b') 
            linha = linha + r.campo(n.produto.unid2, 8, 'l') if n.produto.unid2 else linha + r.campo('', 8, 'b')
            r.linha(linha)
 
    return r.rel()


