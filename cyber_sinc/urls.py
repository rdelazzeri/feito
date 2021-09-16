from django.urls import path

from . import views as v

app_name = 'cyber_sinc'

urlpatterns = [
    path('', v.cyber_sinc, name = 'cyber_sinc'),
    path('sinc_prod', v.prod_sinc_cyber, name = 'prod_sinc_cyber'),
    path('sinc_grupos', v.cyber_sinc_grupos, name = 'cyber_sinc_grupos'),
    path('sinc_unid', v.cyber_sinc_unid, name = 'cyber_sinc_unid '),
    path('sinc_ncm', v.cyber_sinc_ncm, name = 'cyber_sinc_ncm'),
    path('sinc_composicao', v.cyber_sinc_composicao, name = 'cyber_sinc_composicao'),
]