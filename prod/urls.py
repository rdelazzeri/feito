from django.urls import path

from . import views as v

app_name = 'prod'

urlpatterns = [
    path('', v.prod_detail, name = 'prod_detail'),
    path('s', v.prod_list, name = 'prod_list'),
    path('n', v.prod_new, name = 'prod_new'),
    path('p<prod_id>', v.prod_detail, name = 'prod_detail'),
    path('comp/<produto_id>', v.prodcomp, name='prodcomp')
    #path('prodcomp', v.Prod_Create, name = 'prod_create'),
    #path('prodcompup', v.Prod_Update, name = 'prod_update'),
    #path('sinc_unid', v.cyber_sinc_unid, name = 'cyber_sinc_unid '),
    #path('sinc_ncm', v.cyber_sinc_ncm, name = 'cyber_sinc_ncm'),
]