from django.urls import path

from . import views as v

app_name = 'cyber_sinc'

urlpatterns = [
    path('', v.cyber_sinc, name = 'cyber_sinc'),
    path('sincprod', v.prod_sinc_cyber, name = 'prod_sinc_cyber'),
    path('sincgrupos', v.cyber_sinc_grupos, name = 'cyber_sinc_grupos'),
    path('sincunid', v.cyber_sinc_unid, name = 'cyber_sinc_unid'),
    path('sincncm', v.cyber_sinc_ncm, name = 'cyber_sinc_ncm'),
    path('sinccomposicao', v.cyber_sinc_composicao, name = 'cyber_sinc_composicao'),
    path('sincpessoa', v.cyber_sinc_pessoa, name = 'cyber_sinc_pessoa'),
    path('sincoperacao', v.cyber_sinc_operacao, name = 'cyber_sinc_operacao'),
    path('sinc_nf_e', v.cyber_sinc_nf_e, name = 'cyber_sinc_nf_e'),
    path('sinc_nf_ei', v.cyber_sinc_nf_ei, name = 'cyber_sinc_nf_ei'),
    path('sincoperacao_saida', v.cyber_sinc_operacao_saida, name = 'cyber_sinc_operacao_saida'),
    path('sinc_nf_s', v.cyber_sinc_nf_s, name = 'cyber_sinc_nf_s'),
    path('sinc_nf_si', v.cyber_sinc_nf_si, name = 'cyber_sinc_nf_si'),
]