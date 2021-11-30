from django.urls import path

from . import views as v

app_name = 'comercial'

urlpatterns = [
    path('', v.pedidos_list, name = 'pedidos_list'),
    #path('s', v.prod_list, name = 'prod_list'),
    path('n', v.pedido_new, name = 'pedido_new'),
    path('detail/<ped_id>', v.pedido_detail, name = 'pedido_detail'),
    path('read/<int:pk>', v.Pedido_read.as_view(), name = 'pedido_read'),
    path('update/<int:pk>', v.Pedido_update.as_view(), name='pedido_update'),
    path('delete/<int:pk>', v.Pedido_delete.as_view(), name='pedido_delete'),
    path('filter/', v.Pedido_filter.as_view(), name='pedido_filter'),
    path('create/', v.Pedido_create.as_view(), name='pedido_create'),
    path('pedidos/', v.pedidos, name='pedidos'),
    #path('comp/<produto_id>', v.prod_comp, name='prod_comp')
    #path('prodcomp', v.Prod_Create, name = 'prod_create'),
    #path('prodcompup', v.Prod_Update, name = 'prod_update'),
    #path('sinc_unid', v.cyber_sinc_unid, name = 'cyber_sinc_unid '),
    #path('sinc_ncm', v.cyber_sinc_ncm, name = 'cyber_sinc_ncm'),
]