from django.urls import path

from . import views as v

app_name = 'comercial'

urlpatterns = [
    path('', v.pedidos_list, name = 'pedidos_list'),
    #path('s', v.prod_list, name = 'prod_list'),
    path('n', v.pedidos_new, name = 'pedidos_new'),
    #path('del', v.prod_delete, name = 'prod_delete'),
    path('p<ped_id>', v.pedido_detail, name = 'pedido_detail'),
    #path('comp/<produto_id>', v.prod_comp, name='prod_comp')
    #path('prodcomp', v.Prod_Create, name = 'prod_create'),
    #path('prodcompup', v.Prod_Update, name = 'prod_update'),
    #path('sinc_unid', v.cyber_sinc_unid, name = 'cyber_sinc_unid '),
    #path('sinc_ncm', v.cyber_sinc_ncm, name = 'cyber_sinc_ncm'),
]