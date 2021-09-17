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
]